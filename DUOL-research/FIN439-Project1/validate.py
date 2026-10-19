"""Independent identities, source checks and deliberately broken-model tests."""
import copy,csv,json,math,re,importlib.util,sys,subprocess,time,urllib.request,urllib.error,os
from html import unescape
from model import ROOT,run,load_data,assumptions,valuation,PRICE

def validate_model(data):
    base=data['base'];a=base['assumptions'];h,interim=load_data();v=base['valuation'];tests=[]
    def check(name,condition,detail):
        tests.append(dict(test=name,status='PASS' if condition else 'FAIL',detail=str(detail)))
        if not condition:raise AssertionError(name+': '+str(detail))
    spec=importlib.util.spec_from_file_location('abg',ROOT/'evidence/abg_known_answer.py');abg=importlib.util.module_from_spec(spec);spec.loader.exec_module(abg)
    known=abg.value(abg.project())['value_per_share'];check('Lab 09 independent known-answer',abs(known-291.75)<.005,known)
    original=140.18321713393624
    check('Lab valuation lineage explicitly differs',abs(v['value_per_share']-original)>1,'Original Lab10 140.18321713393624; corrected engine '+str(v['value_per_share'])+'; not a single-factor attribution')
    for key,amount in [('fcff',100.),('cash',10.),('ar',5.),('period_cfo',1.),('ppe',2.),('period_repurchase_settlement',.675),('period_withholding',1.)]:
        broken=copy.deepcopy(base['statements']);broken[0][key]+=amount
        try:valuation(broken,h,interim,a);blocked=False
        except ValueError:blocked=True
        check('Reject corrupted '+key,blocked,'Deliberately changed first forecast line by '+str(amount)+'m; required refusal')
    for key,value in [('terminal_growth',a['wacc'][0]),('terminal_growth',a['wacc'][0]+.01),('diluted_shares',0),('minimum_cash',100000),('growth',float('nan')),('growth',[.1]),('growth',True),('buybacks',-1),('wacc',[.08,.09,.09,.09,.09]),('gross_margin',1.1)]:
        try:run({key:value});blocked=False
        except (ValueError,ZeroDivisionError,OverflowError):blocked=True
        check('Invalid assumption '+key+'='+str(value),blocked,'Valuation must not be returned')
    for r in sorted(set(x['wacc'] for x in data['grid'])):
        values=[x['value_per_share'] for x in data['grid'] if x['wacc']==r]
        check('Growth grid monotonicity at WACC '+str(r),all(y>x for x,y in zip(values,values[1:])),'Value increases as perpetual growth increases in this bounded grid')
    for g in sorted(set(x['terminal_growth'] for x in data['grid'])):
        values=[x['value_per_share'] for x in data['grid'] if x['terminal_growth']==g]
        check('WACC grid monotonicity at g '+str(g),all(y<x for x,y in zip(values,values[1:])),'Value decreases as discount rate increases')
    first=base['statements'][0]
    # Independently work BACK from December cash by removing cash flows after September.
    recurring_h2=first['period_cfo']+first['period_cfi']+first['period_cff']+2.297
    september_cash=first['cash']-101/184*recurring_h2
    expected_excess=september_cash+interim['short_investments']+interim['long_investments']-a['minimum_cash'][0]
    check('Dated cash agrees with year-end rollback',abs(v['estimated_dated_cash']-september_cash)<1e-8,september_cash)
    check('Repurchase recognition versus settlement',abs(v['new_post_h1_repurchases']-(71.9-70.278))<1e-8 and abs(v['settlement_of_h1_repurchases']-(70.278-69.603))<1e-8,'1.622m new trades plus 0.675m opening payable; settlement assumption disclosed')
    check('Financing payable excluded from operating NWC',abs(first['delta_nwc']-(first['nwc']-interim['nwc']-.675))<1e-8,'Opening operating NWC excludes repurchase payable')
    check('Settlement does not reduce equity twice',abs(first['equity']-(interim['equity']+first['period_net_income']+first['period_sbc']+first['period_cff']+.675))<1e-8,'June equity already reflects unsettled purchases')
    old_excess=interim['cash']+interim['investments']+83/184*(first['fcff']+first['period_interest_income']*(1-a['tax_rate'][0]))-2.297-a['minimum_cash'][0]
    check('Reject economic FCFF as cash accumulation',abs(old_excess-expected_excess)>1,'Old SBC-expensed cash proxy fails statement-based reconciliation')
    independent_ev=sum(x['future_fcff']/((1+v['wacc'])**x['period']) for x in v['discounted'])+v['terminal_fcff']/(v['wacc']-v['terminal_growth'])/((1+v['wacc'])**v['discounted'][-1]['period'])
    check('Independent DCF sum',abs(independent_ev-v['enterprise_value'])<1e-8,independent_ev)
    for case in data['cases']:
        check('Causal case finite '+case['case'],math.isfinite(case['value_per_share']) and case['value_per_share']>0,case['value_per_share'])
    check('Causal case ordering',data['cases'][0]['value_per_share']<v['value_per_share']<data['cases'][2]['value_per_share'],'Low < Base < High')
    def bridge_ok(proposed_equity):return abs(proposed_equity-(v['enterprise_value']+expected_excess))<1e-7
    check('Independent dated cash bridge',bridge_ok(v['equity_value']),expected_excess)
    future_cash=base['statements'][-1]['cash']
    check('Reject future cash double-count',not bridge_ok(v['equity_value']+future_cash),'Adding '+str(future_cash)+'m of terminal cash violates the independent bridge')
    check('Per-share bridge',abs(v['value_per_share']*a['diluted_shares'][0]-v['equity_value'])<1e-7,'Equity / positive diluted shares')
    # Expectations are written here before these automated executions, not human precommit evidence.
    for key,shock,direction in [('growth',.01,1),('gross_margin',.01,1),('sbc_ratio',.01,-1),('wacc',.01,-1),('terminal_growth',.005,1)]:
        changed=run({key:[x+shock for x in a[key]]})['valuation']['value_per_share'];delta=changed-v['value_per_share']
        check('Automated direction '+key,delta*direction>0,'Shock '+str(shock)+' decimal; expected '+str(direction)+'; actual delta/share '+str(delta))
    check('Exact restored base',abs(run()['valuation']['value_per_share']-v['value_per_share'])<1e-10,'No shared input mutation')
    # The two original Lab11 narratives both target the identical growth vector.
    paid=run({'growth':[x+.01 for x in a['growth']]});ai=run({'growth':[x+.01 for x in a['growth']]})
    check('Equal growth-channel shocks are identical',paid['valuation']==ai['valuation'],'Naming a shock AI does not create an independent economic mechanism')
    facts=json.loads((ROOT/'data/sources/annual_inline_xbrl.json').read_text(encoding='utf8'))['facts']
    for key,tag in [('revenue','RevenueFromContractWithCustomerExcludingAssessedTax'),('ebit','OperatingIncomeLoss'),('net_income','NetIncomeLoss'),('cfo','NetCashProvidedByUsedInOperatingActivities'),('sbc','ShareBasedCompensation')]:
        values=[f['value_millions'] for f in facts if f['tag']=='us-gaap:'+tag and f['end']=='2025-12-31' and f['start']=='2025-01-01' and not f['dimensional']]
        check('Independent XBRL source '+key,any(abs(x-h[2025][key])<1e-6 for x in values),'Retained filing facts vs working CSV: '+str(values))
    companyfacts=json.loads((ROOT/'data/sources/companyfacts.json').read_text(encoding='utf8'))['facts']['us-gaap']
    for tag,amount in [('TreasuryStockValueAcquiredCostMethod',70.278),('PaymentsForRepurchaseOfCommonStock',69.603)]:
        source_values=[x['val']/1e6 for values in companyfacts[tag]['units'].values() for x in values if x.get('start')=='2026-01-01' and x['end']=='2026-06-30' and x.get('filed','9999')<='2026-09-21']
        check('Repurchase primary-source '+tag,any(abs(x-amount)<1e-8 for x in source_values),source_values)
    n=data['normalization'];b=h[2025]
    check('Reported FCF definition',abs(n['reported_fcf']-(387.823-18.096-9.303))<1e-8,'Includes software AND PPE investment; not an FCFF substitution')
    reconciled=b['net_income']-b['other_net']+b['tax']-(b['ebit']+b['interest_income'])*.24
    check('Normalized earnings bridge',abs(reconciled-n['normalized_earnings'])<1e-8,reconciled)
    for row in data['multiples']:
        check('Multiple arithmetic '+row['multiple'],abs(row['market_numerator_m']/row['denominator_m']-row['market_multiple'])<1e-9,'Same dated diluted convention; denominator '+str(row['denominator_m']))
    check('EBITDA retains SBC',abs(data['multiples'][1]['denominator_m']-(135.570+14.391))<1e-8,'GAAP EBIT plus D&A only')
    def text(html):return ' '.join(unescape(re.sub('<[^>]+>',' ',html)).split())
    release=(ROOT/'data/sources/cour-fy2025-results.html').read_text(encoding='utf8')
    eps=[text(row) for row in re.findall(r'<tr[^>]*>(.*?)</tr>',release,re.S|re.I) if 'Net loss per share' in text(row) and 'basic and diluted' in text(row)]
    check('Peer GAAP loss exclusion',any(re.search(r'0\.31\s*\)',row) for row in eps),'Annual GAAP negative EPS; not adjusted EPS')
    merger=text((ROOT/'data/sources/cour-merger-2026-05-11.html').read_text(encoding='utf8'))
    check('Peer entity-scope exclusion',all(s in merger for s in ['May 11, 2026','wholly owned subsidiary','0.800']),'UDMY converted; combined COUR numerator cannot use old standalone denominator')
    for r in data['reverse_dcf']:check('Reverse DCF '+r['driver'],r['status']=='SOLVED' and abs(r['value']-PRICE)<1e-6,r)
    return tests

def panel_checks():
    port=18765;env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
    proc=subprocess.Popen([sys.executable,'-B',str(ROOT/'panel.py'),'--port',str(port)],cwd=ROOT,env=env,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
    results=[]
    try:
        for _ in range(100):
            try:urllib.request.urlopen(f'http://127.0.0.1:{port}',timeout=2);break
            except OSError:time.sleep(.1)
        def request(name,payload,status=200,path='/value'):
            req=urllib.request.Request(f'http://127.0.0.1:{port}'+path,data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
            try:
                with urllib.request.urlopen(req) as response:code=response.status;data=json.load(response)
            except urllib.error.HTTPError as error:code=error.code;data=json.load(error)
            assert code==status,(name,code,data)
            assert (data.get('all_pass') is True) if status==200 else ('error' in data and 'value_per_share' not in data)
            results.append(dict(test=name,status='PASS',http_status=code,value=data.get('value_per_share')));return data
        base=request('Base',{});high=request('Margin +1pp',{'margin':1});assert high['value_per_share']>base['value_per_share']
        reset=request('Reset',{});assert abs(reset['value_per_share']-base['value_per_share'])<1e-9
        request('Real DCF failure',{},422,'/failure-test')
        for name,payload in [('Out of bounds',{'growth':3.01}),('NaN',{'growth':float('nan')}),('Infinity',{'wacc':float('inf')}),('String',{'growth':'1'}),('Boolean',{'margin':True}),('Unknown field',{'cash':0}),('Nonobject',[])]:request(name,payload,422)
        from panel import CONTROLS
        for key,c in CONTROLS.items():
            for side in ['low','high']:request(key+' '+side,{key:c[side]})
        import itertools
        for sides in itertools.product(['low','high'],repeat=len(CONTROLS)):
            request('Combined endpoints '+','.join(sides),{key:CONTROLS[key][side] for key,side in zip(CONTROLS,sides)})
        restored=request('Final recovery',{});assert abs(restored['value_per_share']-base['value_per_share'])<1e-9
        (ROOT/'evidence/panel-checks.json').write_text(json.dumps(results,indent=2),encoding='utf8');print('PASS:',len(results),'panel checks')
    finally:proc.terminate();proc.wait(timeout=10)

if __name__=='__main__':
    if '--panel' in sys.argv:panel_checks()
    else:
        from analysis import compute
        results=validate_model(compute());print('PASS:',len(results),'validation tests')
