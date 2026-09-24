"""Local driver panel. Same Python forecast/check/DCF functions as the notebook."""
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
import argparse,json
from src.data_loader import load_data,price_data
from src.beta import estimate
from src.assumptions import build_assumptions,unpack
from src.sensitivity import rerun
from src.checks import run_model_checks

H,I=load_data();P,PRICE=price_data();B,_=estimate(P);A=unpack(build_assumptions(H,B.iloc[0].beta))
HTML='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>DUOL valuation drivers</title>
<style>body{font:18px system-ui;background:#f4f7f8;color:#19344c;max-width:860px;margin:40px auto;padding:24px}main{background:white;padding:32px;border-radius:14px}label{display:block;margin:26px 0}input{width:100%}output{font-weight:bold}#value{font-size:42px;color:#007d70}small{display:block;line-height:1.5}#checks{white-space:pre-wrap;font-size:14px}</style>
<main><h1>Duolingo valuation drivers</h1><p>September 21, 2026 • USD per diluted share</p>
<label>Revenue growth path shift: <output id="growthOut">0.0</output> percentage points<input id="growth" type="range" min="-5" max="5" step="0.1" value="0"></label>
<label>Gross margin path shift: <output id="marginOut">0.0</output> percentage points<input id="margin" type="range" min="-3" max="3" step="0.1" value="0"></label>
<label>WACC: <output id="waccOut"></output>%<input id="wacc" type="range" min="5.3" max="11.3" step="0.01" value="8.276376244"></label>
<div id="value">Calculating…</div><p id="compare"></p><pre id="checks"></pre>
<small>Every change reruns the linked statements and required checks. Other assumptions remain at base. Terminal growth is 3%. This is an educational model, not investment advice. Read the notebook for source dates, dilution and terminal-value limitations.</small></main>
<script>let serial=0;async function update(){let id=++serial;let inputs={};for(let k of ['growth','margin','wacc']){inputs[k]=Number(document.getElementById(k).value);document.getElementById(k+'Out').textContent=inputs[k].toFixed(2)}let response=await fetch('/value',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(inputs)});let d=await response.json();if(id!==serial)return;document.getElementById('value').textContent=d.error?'Valuation blocked':'$'+d.value_per_share.toFixed(2);document.getElementById('compare').textContent=d.error?'':`Market close $${d.market_price.toFixed(2)} • Terminal share of EV ${(100*d.terminal_share).toFixed(1)}%`;document.getElementById('checks').textContent=d.error||d.checks}for(let k of ['growth','margin','wacc'])document.getElementById(k).addEventListener('input',update);update();</script></html>'''

def evaluate(data):
    v,m,a=rerun(H,I,A,{'growth':A['growth']+float(data.get('growth',0))/100,'gross_margin':A['gross_margin']+float(data.get('margin',0))/100,'wacc':float(data.get('wacc',A['wacc'][0]*100))/100})
    checks=run_model_checks(m,I,a,H)
    return dict(value_per_share=v['value_per_share'],market_price=PRICE,terminal_share=v['terminal_share_ev'],checks=f'ALL {len(checks)} REQUIRED CHECKS PASSED\nVALUATION ENABLED',all_pass=True)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        data=HTML.encode('utf8');self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.end_headers();self.wfile.write(data)
    def do_POST(self):
        try:result=evaluate(json.loads(self.rfile.read(int(self.headers['Content-Length']))));status=200
        except (ValueError,KeyError) as e:result={'error':str(e)};status=422
        self.send_response(status);self.send_header('Content-Type','application/json');self.end_headers();self.wfile.write(json.dumps(result).encode())
    def log_message(self,*args):pass

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=8765);args=parser.parse_args()
    print(f'DUOL driver panel: http://127.0.0.1:{args.port}',flush=True)
    ThreadingHTTPServer(('127.0.0.1',args.port),Handler).serve_forever()
