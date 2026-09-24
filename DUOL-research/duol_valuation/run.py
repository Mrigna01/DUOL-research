"""Build every computational deliverable from immutable local inputs."""
from pathlib import Path
import sys,os,json,hashlib,subprocess,urllib.request,time,zipfile,asyncio
from importlib.metadata import version
from bs4 import BeautifulSoup
import nbformat
from nbclient import NotebookClient
from nbconvert import HTMLExporter
from src.pipeline import run_analysis
from src.notebook_builder import build_notebook
from src.data_loader import ROOT

def panel_smoke_test(base):
    # The helper runs hidden on Windows and is terminated in finally.
    port=18765
    proc=subprocess.Popen([sys.executable,str(ROOT/'panel.py'),'--port',str(port)],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,
                          creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
    try:
        deadline=time.monotonic()+40
        while True:
            try:
                html=urllib.request.urlopen(f'http://127.0.0.1:{port}',timeout=2).read().decode();break
            except OSError:
                if proc.poll() is not None:raise RuntimeError(proc.stderr.read().decode())
                if time.monotonic()>deadline:raise TimeoutError('Panel did not start')
                time.sleep(.2)
        assert '<input' in html and 'Gross margin' in html
        results=[]
        for label,margin in [('base',0),('gross margin +1pp',1)]:
            body=json.dumps({'growth':0,'margin':margin,'wacc':base['wacc']*100}).encode()
            req=urllib.request.Request(f'http://127.0.0.1:{port}/value',data=body,headers={'Content-Type':'application/json'})
            result=json.load(urllib.request.urlopen(req,timeout=20));assert result['all_pass'];results.append(dict(move=label,**result))
        assert abs(results[0]['value_per_share']-base['value_per_share'])<1e-8
        assert results[1]['value_per_share']>results[0]['value_per_share']
        (ROOT/'outputs/tables/panel_smoke_test.json').write_text(json.dumps(results,indent=2),encoding='utf8')
    finally:
        proc.terminate();proc.wait(timeout=10)

def main():
    if sys.platform=='win32' and sys.version_info<(3,14):asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    print('Building model, enforced checks, scenarios, roots, audit and charts...',flush=True)
    d=run_analysis()
    print('Executing the complete notebook...',flush=True)
    nb=build_notebook()
    NotebookClient(nb,timeout=300,kernel_name='python3',resources={'metadata':{'path':str(ROOT)}}).execute()
    nbformat.write(nb,ROOT/'duol_valuation.ipynb')
    assert not any(o.output_type=='error' for c in nb.cells if c.cell_type=='code' for o in c.get('outputs',[]))
    exporter=HTMLExporter();body,_=exporter.from_notebook_node(nb)
    rendered=BeautifulSoup(body,'html.parser')
    assert '25. Conclusion' in rendered.get_text() and len(rendered.find_all('img'))>=7
    (ROOT/'outputs/duol_valuation.html').write_text(body,encoding='utf8')
    print('Testing local panel HTTP response and a driver move...',flush=True)
    panel_smoke_test(d['v'])
    hashes=[dict(file=str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size) for p in sorted((ROOT/'data/raw').rglob('*')) if p.is_file()]
    (ROOT/'outputs/tables/source_hashes.json').write_text(json.dumps(hashes,indent=2))
    record={'status':'PASS','python':sys.version,'dependencies':{x:version(x) for x in ['numpy','pandas','scipy','matplotlib','nbformat','nbclient','nbconvert','ipykernel','tabulate','beautifulsoup4']},'checks':len(d['checks']),'deliberate_failures_blocked':len(d['broken']),
            'independent_audit_checks':len(d['audit']),'abg_reference_checks':len(d['abg']),
            'notebook_code_cells':sum(c.cell_type=='code' for c in nb.cells),'notebook_errors':0,'figures':len(d['figures']),
            'sensitivity_drivers':len(d['shocks']),'discount_rates':len(d['rates']),'implied_roots':int(d['implied'].market_implied.notna().sum()),
            'value_per_share':d['v']['value_per_share']}
    (ROOT/'outputs/tables/run_status.json').write_text(json.dumps(record,indent=2))
    archive=ROOT.parent/'duol_valuation_submission.zip'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for p in ROOT.rglob('*'):
            if p.is_file() and '__pycache__' not in p.parts and '.ipynb_checkpoints' not in p.parts:z.write(p,p.relative_to(ROOT.parent))
    print(json.dumps(record,indent=2));print(f'Submission bundle: {archive}')

if __name__=='__main__':main()
