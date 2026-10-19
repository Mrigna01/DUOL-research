"""Bounded valuation interface; accounting and sources stay in model.py."""
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from urllib.parse import urlsplit,unquote
import argparse,json,math,mimetypes
from model import ROOT,PRICE,run,assumptions
A=assumptions();BASE=run()['valuation']['value_per_share']
CASE_VALUES=[run({'growth':[x+.03*t for x in A['growth']], 'gross_margin':[x+.01*t for x in A['gross_margin']], 'rd_ex_sbc':[x-.01*t for x in A['rd_ex_sbc']]})['valuation']['value_per_share'] for t in [-1,0,1]]
CONTROLS={
 'growth':dict(label='Revenue growth path shift',unit='percentage points',low=-3.,high=3.,base=0.,reason='Earlier sensitivity tests used +/-1 and +/-2pp. The +/-3pp stress also tests the forecast recovery. Judgment range, not a probability or independently measured AI contribution.'),
 'margin':dict(label='Gross margin path shift',unit='percentage points',low=-1.,high=1.,base=0.,reason='AI delivery-cost stress: +/-1pp. Tests inference/delivery costs separately from revenue; anchored to 71.6% first-year guidance.'),
 'sbc':dict(label='SBC / revenue path shift',unit='percentage points',low=-2.,high=2.,base=0.,reason='Compensation intensity stress around 15% first-year guidance and a declining path. +/-2pp is analyst judgment; SBC remains an economic cost.'),
 'wacc':dict(label='WACC',unit='percent',low=A['wacc'][0]*100-3,high=A['wacc'][0]*100+3,base=A['wacc'][0]*100,reason='CAPM-based WACC +/-3pp tests discount-rate uncertainty. This is a judgment stress, not a confidence interval.'),
 'terminal':dict(label='Terminal growth',unit='percent',low=2.,high=4.,base=3.,reason='Lab 6 grid: 2%-4% nominal growth. High end is demanding; growth must remain below WACC.')}

def evaluate(data):
 if not isinstance(data,dict):raise ValueError('Expected an object')
 if set(data)-set(CONTROLS)-{'sensitivity_driver'}:raise ValueError('Unknown or locked input')
 inputs={}
 for key,c in CONTROLS.items():
  x=data.get(key,c['base'])
  if isinstance(x,bool) or not isinstance(x,(float,int)) or not math.isfinite(x):raise ValueError(key+': a finite number is required')
  if not c['low']-1e-10<=x<=c['high']+1e-10:raise ValueError(key+': outside the bounded range')
  inputs[key]=x
 driver=data.get('sensitivity_driver','growth')
 if not isinstance(driver,str) or driver not in CONTROLS:raise ValueError('Invalid sensitivity driver')
 def calculate(x):return run({'growth':[v+x['growth']/100 for v in A['growth']],'gross_margin':[v+x['margin']/100 for v in A['gross_margin']],'sbc_ratio':[v+x['sbc']/100 for v in A['sbc_ratio']],'wacc':x['wacc']/100,'terminal_growth':x['terminal']/100})
 result=calculate(inputs);v=result['valuation'];rows=result['statements'];sweep=[]
 for case in ['low','base','high']:
  x={key:c['base'] for key,c in CONTROLS.items()};x[driver]=CONTROLS[driver][case];s=calculate(x)
  sweep.append(dict(case=case,input=x[driver],ebit_2030=s['statements'][-1]['ebit'],fcff_2030=s['statements'][-1]['fcff'],value_per_share=s['valuation']['value_per_share'],change_from_base=s['valuation']['value_per_share']-BASE))
 groups={'Income statement ($m)':['revenue','gross_profit','rd','sm','ga','ebit','interest_income','other_net','pretax','tax','net_income'],'Balance sheet ($m)':['cash','short_investments','long_investments','ar','deferred_cost','prepaid','ppe','intangibles','assets','ap','accrued','deferred_revenue','liabilities','equity'],'Cash flow ($m)':['net_income','da','sbc','cfo','cfi','cff','cash','annual_fcff']}
 statements={title:[dict(line=k,values=[r[k] for r in rows]) for k in fields] for title,fields in groups.items()}
 return dict(value_per_share=v['value_per_share'],base_value=BASE,change_from_base=v['value_per_share']-BASE,market_price=PRICE,terminal_share=v['terminal_share'],all_pass=True,checks=f"ALL {len(result['checks'])} MODEL CHECKS PASSED",check_rows=[dict(check_name=r['test'],year=r['year'],status=r['status']) for r in result['checks']],sensitivity_driver=driver,sensitivity=sweep,statements=statements,years=[r['year'] for r in rows],bridge={k:v[k] for k in ['enterprise_value','excess_cash','debt','equity_value','diluted_shares']})

def required_failure_test():
 try:run({'terminal_growth':A['wacc'][0]})
 except ValueError as exc:return dict(error='DELIBERATE FAILURE TEST: terminal growth = WACC. '+str(exc),all_pass=False)
 raise RuntimeError('Failure test unexpectedly returned a value')

HTML="""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>DUOL Valuation Workbench</title>
<style>body{font:16px system-ui;color:#173042;background:#f4f6f7;margin:0}main{max-width:1100px;margin:auto;padding:24px}section{background:white;border:1px solid #d4dce1;padding:20px;margin:18px 0;border-radius:6px}.controls{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px}label{display:block;font-weight:600}input{width:100%;margin:12px 0}small{display:block;line-height:1.5;color:#415766}button,select{font:inherit;padding:9px 12px;margin:8px 8px 8px 0;cursor:pointer}#value{font-size:36px;font-weight:700}.pass{color:#126048;background:#e6f4ed}.fail{color:#9b2020;background:#ffeded}.status{padding:12px;white-space:pre-wrap}table{border-collapse:collapse;width:100%;font-size:14px}th,td{text-align:right;padding:8px;border-bottom:1px solid #dfe5e9}th:first-child,td:first-child{text-align:left}.scroll{overflow:auto}details{margin:16px 0}a{color:#145d8b}</style></head>
<body><main><h1>Duolingo valuation workbench</h1><p>September 21, 2026 | USD per diluted share | Five-year FCFF valuation</p><p>Test assumptions through linked five-year statements and FCFF DCF. Sources, accounting and checks stay locked. Scenario analysis; not investment advice.</p>
<section id="baseDecision"><h2>Base decision: Watch / Defer</h2><p>Investment horizon: 3-5 years. September 21, 2026 market price: $149.42.</p><p><strong>Base operating scenarios: __CASE_VALUES__ per share.</strong></p><p>This fixed reference range uses the documented low/base/high operating cases. The live what-if valuation below changes with your controls; it does not automatically revise the recommendation.</p></section><section><div class="controls" id="controls"></div><button id="reset" type="button">Reset to base</button><button id="failure" type="button">Test failure: terminal growth = WACC</button><small>The failure test sends an incoherent input to a copy of the actual DCF. Reset restores all base assumptions and recalculates. Bounds are judgment stress ranges, explained above.</small></section>
<section aria-live="polite"><h2>Live what-if valuation</h2><div id="value">Calculating...</div><p id="comparison"></p><p id="terminalShare"></p><div id="checks" class="status"></div><div id="bridge"></div></section>
<section><h2>One driver at a time</h2><label for="driver">Compare lower/base/higher inputs</label><select id="driver"></select><p id="sensitivityLabel"></p><small>Only the selected driver changes in this table; all others reset to the original base. Ranking depends on the chosen ranges. The live value above can include several simultaneous changes.</small><div id="sensitivity" class="scroll"></div></section>
<section><h2>Linked five-year statements</h2><small>Annual 2026 amounts include filed H1 and forecast H2. Only cash flow after September 21 enters DCF. Annual analytical FCFF uses normalized taxes and is not reported company FCF.</small><div id="statements"></div><details><summary>All model checks</summary><div id="checkTable" class="scroll"></div></details></section>
<p><a href="/analysis">Executed analysis, cases and valuation range</a> | <a href="/validation">Validation and AI-use record</a></p></main>
<script>
const config=__CONFIG__;let serial=0;let timer;
const money=x=>'$'+(Math.abs(Number(x))<0.005?0:Number(x)).toFixed(2);const number=x=>Number(x).toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2});
function table(headers,rows){let t=document.createElement('table'),tr=document.createElement('tr');headers.forEach(h=>{let th=document.createElement('th');th.textContent=h;tr.append(th)});t.append(tr);rows.forEach(row=>{let tr=document.createElement('tr');row.forEach(x=>{let td=document.createElement('td');td.textContent=x;tr.append(td)});t.append(tr)});return t}
function clearResults(message,failed=false){document.getElementById('value').textContent=message;for(let k of ['comparison','terminalShare','bridge','sensitivity','statements','checkTable','sensitivityLabel'])document.getElementById(k).replaceChildren();let e=document.getElementById('checks');e.textContent=failed?message:'Recalculating; previous results cleared.';e.className='status '+(failed?'fail':'')}
function values(){let v={sensitivity_driver:document.getElementById('driver').value};for(let k in config)v[k]=Number(document.getElementById(k).value);return v}
function labels(){for(let k in config)document.getElementById(k+'Out').textContent=Number(document.getElementById(k).value).toFixed(2)+' '+config[k].unit}
async function update(failure=false){clearTimeout(timer);let id=++serial;labels();clearResults('Calculating...');try{let response=await fetch(failure?'/failure-test':'/value',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(failure?{}:values())});let d=await response.json();if(id!==serial)return;if(!response.ok||d.error||!d.all_pass){clearResults(d.error||'Valuation blocked: invalid response.',true);return}document.getElementById('value').textContent=money(d.value_per_share);document.getElementById('comparison').textContent=`Base ${money(d.base_value)} | Change ${money(d.change_from_base)} | Dated market ${money(d.market_price)}`;document.getElementById('terminalShare').textContent=`Terminal value: ${(100*d.terminal_share).toFixed(2)}% of enterprise value`;let c=document.getElementById('checks');c.textContent=d.checks;c.className='status pass';let b=d.bridge;document.getElementById('bridge').append(table(['Bridge ($m except shares)','Value'],[['Enterprise value',number(b.enterprise_value)],['Estimated excess cash',number(b.excess_cash)],['Debt',number(b.debt)],['Equity value',number(b.equity_value)],['Diluted shares (m)',number(b.diluted_shares)]]));document.getElementById('sensitivityLabel').textContent=config[d.sensitivity_driver].label+'; other inputs at base';document.getElementById('sensitivity').append(table(['Case','Input','2030 EBIT ($m)','2030 FCFF ($m)','Value/share','Change'],d.sensitivity.map(x=>[x.case,number(x.input),number(x.ebit_2030),number(x.fcff_2030),money(x.value_per_share),money(x.change_from_base)])));for(let [title,rows] of Object.entries(d.statements)){let h=document.createElement('h3');h.textContent=title;let div=document.createElement('div');div.className='scroll';div.append(table(['Line',...d.years],rows.map(x=>[x.line,...x.values.map(number)])));document.getElementById('statements').append(h,div)}document.getElementById('checkTable').append(table(['Check','Year','Status'],d.check_rows.map(x=>[x.check_name,x.year,x.status])))}catch(e){if(id===serial)clearResults('Valuation unavailable: '+e.message+'. Check the server, then reset.',true)}}
for(let [k,s] of Object.entries(config)){let div=document.createElement('div'),label=document.createElement('label');label.htmlFor=k;label.textContent=s.label;let out=document.createElement('output');out.id=k+'Out';let input=document.createElement('input');Object.assign(input,{id:k,type:'range',min:s.low,max:s.high,step:0.01,value:s.base});let note=document.createElement('small');note.textContent=s.reason;div.append(label,out,input,note);document.getElementById('controls').append(div);let option=document.createElement('option');option.value=k;option.textContent=s.label;document.getElementById('driver').append(option);input.addEventListener('input',()=>{++serial;labels();clearResults('Recalculating...');clearTimeout(timer);timer=setTimeout(()=>update(),120)})}
document.getElementById('reset').addEventListener('click',()=>{for(let [k,s] of Object.entries(config))document.getElementById(k).value=s.base;document.getElementById('driver').value='growth';update()});document.getElementById('failure').addEventListener('click',()=>update(true));document.getElementById('driver').addEventListener('change',()=>update());update();
</script></body></html>""".replace('__CONFIG__',json.dumps(CONTROLS)).replace('__CASE_VALUES__',' / '.join(f'${x:.2f}' for x in CASE_VALUES))

class Handler(BaseHTTPRequestHandler):
 def reply(self,status,data,kind='application/json'):
  payload=data if isinstance(data,bytes) else data.encode('utf8') if isinstance(data,str) else json.dumps(data,allow_nan=False).encode('utf8')
  self.send_response(status);self.send_header('Content-Type',kind+'; charset=utf-8');self.send_header('Cache-Control','no-store');self.send_header('Content-Length',str(len(payload)));self.end_headers();self.wfile.write(payload)
 def do_GET(self):
  path=unquote(urlsplit(self.path).path)
  if path=='/':self.reply(200,HTML,'text/html');return
  aliases={'/analysis':'outputs/visible-output.html','/validation':'docs/validation-and-ai-use.md'}
  relative=aliases.get(path,path.lstrip('/'));p=(ROOT/relative).resolve()
  if p.is_relative_to(ROOT) and relative.split('/')[0] in ['outputs','docs','data','evidence'] and p.is_file():self.reply(200,p.read_bytes(),mimetypes.guess_type(p.name)[0] or 'text/plain')
  else:self.reply(404,dict(error='Not found; run analysis.py first if an output is missing'))
 def do_POST(self):
  if self.path not in ['/value','/failure-test']:self.reply(404,dict(error='Not found'));return
  try:
   n=int(self.headers.get('Content-Length','0'))
   if not 0<n<=8192:raise ValueError('Invalid request size')
   data=json.loads(self.rfile.read(n))
   if self.path=='/failure-test':
    if data!={}:raise ValueError('Failure test expects an empty object')
    self.reply(422,required_failure_test())
   else:self.reply(200,evaluate(data))
  except (ValueError,TypeError,KeyError,OverflowError) as exc:self.reply(422,dict(error='VALUATION BLOCKED: '+str(exc),all_pass=False))
  except Exception:
   self.reply(500,dict(error='VALUATION BLOCKED: calculation failed; inspect server log',all_pass=False))
   import traceback;traceback.print_exc()
 def log_message(self,*args):pass

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=8765);args=parser.parse_args()
 print(f'DUOL workbench: http://127.0.0.1:{args.port}',flush=True)
 ThreadingHTTPServer(('127.0.0.1',args.port),Handler).serve_forever()
