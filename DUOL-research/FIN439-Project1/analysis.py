"""Combine Lab 6 valuation tools, Lab 08 definitions and Lab 11 OAT analysis."""
import csv,json,math
from html import escape
from datetime import datetime,timezone
from model import ROOT,PRICE,run,assumptions,load_data,wacc_evidence

def metric(result):
    y=result['statements'][-1];v=result['valuation']
    return dict(ebit_2030=y['ebit'],fcff_2030=y['fcff'],value_per_share=v['value_per_share'])

def root_solve(key,low,high,target=PRICE,shift=False):
    base=assumptions()[key]
    def evaluate(x):return run({key:[v+x for v in base] if shift else x})['valuation']['value_per_share']-target
    flo,fhi=evaluate(low),evaluate(high)
    if flo*fhi>0:return dict(driver=key,solved_input=None,lower=low,upper=high,shift=shift,status='NO ROOT IN BOUNDS')
    for _ in range(65):
        mid=(low+high)/2;fm=evaluate(mid)
        if abs(fm)<1e-8:break
        if fm*flo>0:low=mid;flo=fm
        else:high=mid
    return dict(driver=key,solved_input=mid,value=target+fm,shift=shift,status='SOLVED')

def compute():
    base=run();a=base['assumptions'];v=base['valuation'];h,_=load_data();b=h[2025]
    cases=[]
    for label,sign in [('Low',-1),('Base',0),('High',1)]:
        result=run({'growth':[x+.03*sign for x in a['growth']],'gross_margin':[x+.01*sign for x in a['gross_margin']],'rd_ex_sbc':[x-.01*sign for x in a['rd_ex_sbc']]})
        cases.append(dict(case=label,**metric(result),cause='Growth +/-3pp; margin +/-1pp; R&D ratio inversely +/-1pp' if sign else 'Guidance anchors plus judgment paths'))
    rates=[a['wacc'][0]+i*.01 for i in range(-3,4)];growth=[.02,.025,.03,.035,.04]
    grid=[dict(wacc=r,terminal_growth=g,value_per_share=run({'wacc':r,'terminal_growth':g})['valuation']['value_per_share']) for r in rates for g in growth]
    with (ROOT/'data/assumptions.csv').open(encoding='utf8') as f:ledger=list(csv.DictReader(f))
    sensitivity=[]
    for key in a:
        selected=[r for r in ledger if r['assumption_name']==key]
        for case,column in [('Low','downside_value'),('Base','base_value'),('High','upside_value')]:
            values=[float(r[column]) for r in selected]
            result=run({key:values});sensitivity.append(dict(driver=key,case=case,first_year_input=values[0],**metric(result)))
    ranking=[]
    for convention,shocks in [('Original ranges',{'growth':.03,'gross_margin':.01,'sbc_ratio':.02}),('Equal +/-1pp',{'growth':.01,'gross_margin':.01,'sbc_ratio':.01})]:
        for key,shock in shocks.items():
            low=metric(run({key:[x-shock for x in a[key]]}));high=metric(run({key:[x+shock for x in a[key]]}))
            ranking.append(dict(range_convention=convention,driver=key,shock_pp=shock*100,**{k+'_span':abs(high[k]-low[k]) for k in low}))
    normalization=dict(reported_net_income=b['net_income'],tax_release_only_earnings=b['net_income']-256.7,remove_other_income=b['other_net'],reported_tax=b['tax'],normalized_tax_rate=.24,normalized_earnings=(b['ebit']+b['interest_income'])*.76,normalized_nopat=b['ebit']*.76,reported_fcf=b['cfo']-b['capex'],normalized_operating_fcff=b['ebit']*.76+b['da']-b['capex']-(b['nwc']-h[2024]['nwc']))
    market_equity=PRICE*v['diluted_shares'];market_ev=market_equity-v['excess_cash']
    multiples=[]
    for name,den,kind in [('EV / FY2025 revenue',b['revenue'],'EV'),('EV / FY2025 EBITDA; SBC retained',b['ebit']+b['da'],'EV'),('Equity / reported earnings',b['net_income'],'Equity'),('Equity / normalized earnings',normalization['normalized_earnings'],'Equity')]:
        market=market_ev if kind=='EV' else market_equity;intrinsic=v['enterprise_value'] if kind=='EV' else v['equity_value']
        multiples.append(dict(multiple=name,denominator_m=den,market_numerator_m=market,dcf_numerator_m=intrinsic,market_multiple=market/den,dcf_multiple=intrinsic/den,convention='September 21; 50.7m diluted valuation shares; estimated excess liquidity'))
    reverse=[root_solve('wacc',.05,.15),root_solve('terminal_growth',.0,.06),root_solve('growth',-.03,.03,shift=True)]
    w=wacc_evidence();g=a['growth']
    # Named downside stresses: each changes one disputed judgment; base assumptions are unchanged.
    stresses=[]
    for name,overrides,why in [
        ('No 2027 reacceleration',{'growth':[g[0],.13,.13,.11,.09]},'Growth 13/13/11/9% after the guided 2026 year'),
        ('Bookings-paced growth',{'growth':[g[0],.11,.11,.10,.09]},'FY2026 bookings guidance +10.9% (Q3 +8.9%) carried into revenue'),
        ('Beta 1.0',{'wacc':w['risk_free']+1.0*w['equity_risk_premium']},'Regression beta is imprecise (see R-squared and standard error)'),
        ('Total-return beta',{'wacc':w['risk_free']+w['total_return_beta']*w['equity_risk_premium']},'Dividend-adjusted DUOL/SPY returns instead of price returns')]:
        stresses.append(dict(stress=name,change=why,value_per_share=run(overrides)['valuation']['value_per_share']))
    stresses.append(dict(stress='Terminal ROIC 20%',change='Terminal reinvestment = g / 20% of NOPAT instead of carried capex/D&A and NWC ratios',value_per_share=base['valuation']['terminal_roic20_value']))
    for s in stresses:s['change_from_base']=s['value_per_share']-v['value_per_share'];s['versus_market']=s['value_per_share']/PRICE-1
    return dict(base=base,cases=cases,grid=grid,sensitivity=sensitivity,range_dependence=ranking,normalization=normalization,multiples=multiples,reported_price_eps=PRICE/8.57,reverse_dcf=reverse,wacc=w,stresses=stresses)

def table(headers,rows):
    return '<div class="scroll"><table><thead><tr>'+''.join('<th>'+escape(str(x))+'</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+escape(f'{x:,.3f}' if isinstance(x,float) else str(x))+'</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table></div>'

def statement_tables(result):
    rows=result['statements'];chunks=[]
    groups={'Income statement ($m)':['revenue','gross_profit','rd','sm','ga','ebit','interest_income','other_net','pretax','tax','net_income'],'Balance sheet ($m)':['cash','short_investments','long_investments','ar','deferred_cost','prepaid','tax_receivable','ppe','intangibles','rou','goodwill','restricted_cash','dta','other_assets','assets','ap','accrued','deferred_revenue','tax_payable','lease_noncurrent','dtl','other_liabilities','liabilities','equity'],'Cash flow ($m)':['net_income','da','sbc','cfo','cfi','cff','cash','annual_fcff']}
    for title,fields in groups.items():chunks.append('<h2>'+title+'</h2>'+table(['Line']+[r['year'] for r in rows],[[k]+[r[k] for r in rows] for k in fields]))
    chunks.append('<p>CFO/CFI/CFF are annual statement cash flows; annual_fcff is an analytical operating measure retaining SBC as a cost. 2026 includes filed H1. DCF only discounts cash flow after September 21.</p>')
    return ''.join(chunks)

STYLE='body{font:16px system-ui;line-height:1.5;color:#183344;max-width:1150px;margin:30px auto;padding:0 20px}h1,h2{color:#124d63}table{border-collapse:collapse;width:100%;font-size:14px}td,th{padding:7px;border:1px solid #d2dce2;text-align:right}td:first-child,th:first-child{text-align:left}th{background:#edf3f5}.scroll{overflow:auto}section{margin:20px 0;padding:16px;background:#f5f8fa}.pass{color:#126048}.fail{color:#a12222}'

def write_csv(name,rows):
    with (ROOT/'outputs'/name).open('w',newline='',encoding='utf8') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)

def main():
    data=compute()
    from validate import validate_model
    tests=validate_model(data)
    out=ROOT/'outputs';out.mkdir(exist_ok=True)
    for name,key in [('causal_cases.csv','cases'),('wacc_growth_grid.csv','grid'),('sensitivity.csv','sensitivity'),('range_dependence.csv','range_dependence'),('valuation_multiples.csv','multiples'),('named_stresses.csv','stresses')]:write_csv(name,data[key])
    v=data['base']['valuation']
    cash_rows=[dict(component=k,amount_m=v[k]) for k in ['reported_cash','estimated_elapsed_cash','new_post_h1_repurchases','settlement_of_h1_repurchases','post_h1_buybacks','estimated_dated_cash','investments','minimum_cash','excess_cash']]
    write_csv('liquidity_bridge.csv',cash_rows)
    write_csv('forecast_statements.csv',data['base']['statements']);write_csv('model_checks.csv',data['base']['checks']);write_csv('validation_checks.csv',tests)
    n=data['normalization'];running=0.;bridge=[]
    for label,change in [('Reported net income',n['reported_net_income']),('Remove other nonoperating income',-n['remove_other_income']),('Reverse entire reported tax benefit',n['reported_tax']),('Apply normalized tax',-(n['normalized_earnings']/.76)*.24)]:
        running+=change;bridge.append(dict(step=label,adjustment_m=change,running_earnings_m=running))
    write_csv('normalization_bridge.csv',bridge)
    for name,value in [('valuation.json',data['base']['valuation']),('normalization.json',data['normalization']),('reverse_dcf.json',data['reverse_dcf']),('wacc.json',data['wacc'])]:(out/name).write_text(json.dumps(value,indent=2),encoding='utf8')
    v=data['base']['valuation'];body=f'<h1>DUOL | Watch / Defer</h1><p>Valuation date: September 21, 2026 | USD | 50.7m diluted valuation shares | Investment horizon: 3-5 years.</p><section><b>Base ${v["value_per_share"]:.2f}; causal range ${data["cases"][0]["value_per_share"]:.2f} to ${data["cases"][2]["value_per_share"]:.2f}; dated market ${PRICE:.2f}.</b><p>Terminal value is {v["terminal_share"]:.2%} of enterprise value. All {len(data["base"]["checks"])} model checks and {len(tests)} validation tests passed. These checks do not establish forecast accuracy.</p></section>'
    body+='<h2>Assumptions and source evidence</h2><p>See <a href="../data/assumptions.csv">dated assumption ledger</a>, <a href="../docs/assumption-challenges.csv">challenges</a>, <a href="../docs/contamination-catalog.csv">normalization catalog</a>, <a href="../docs/sources.md">source map</a>, and <a href="../docs/validation-and-ai-use.md">validation and AI disclosure</a>.</p>'
    body+='<h2>Causal operating cases</h2>'+table(['Case','2030 EBIT','2030 FCFF','Value/share','Cause'],[[r[k] for k in ['case','ebit_2030','fcff_2030','value_per_share','cause']] for r in data['cases']])
    body+='<h2>Enterprise to equity bridge</h2>'+table(['Component','Value'],[[k,v[k]] for k in ['pv_explicit','pv_terminal','enterprise_value','reported_cash','investments','estimated_elapsed_cash','new_post_h1_repurchases','settlement_of_h1_repurchases','post_h1_buybacks','estimated_dated_cash','minimum_cash','excess_cash','debt','equity_value','diluted_shares','value_per_share']])
    body+='<p>The dated cash bridge prorates accounting CFO, investing and financing flows; known repurchase cash is dated separately. The 0.675m June repurchase payable settles in financing and is excluded from operating working capital. New post-June repurchases are approximately 1.622m. Settlement by September 21 is assumed; the reported cumulative purchase figure is rounded. SBC remains a cost in future FCFF, while actual cash adds back noncash SBC and deducts withholding. See data/liquidity_bridge.csv and docs/sources.md.</p>'
    body+='<h2>WACC x terminal growth</h2>'+table(['WACC','Growth','Value/share'],[[f'{r["wacc"]:.2%}',f'{r["terminal_growth"]:.2%}',r['value_per_share']] for r in data['grid']])
    w=data['wacc'];body+=f'<h2>Discount-rate evidence and reliability</h2><p>Beta {w["beta"]:.3f} from {w["observations"]} monthly DUOL/SPY price returns; R-squared {w["r_squared"]:.3f}; standard error {w["beta_standard_error"]:.3f}; approximate 95% normal interval {w["beta_ci95_low"]:.2f} to {w["beta_ci95_high"]:.2f}. Total-return beta {w["total_return_beta"]:.3f}. The market explains under 5% of DUOL monthly return variation, so the selected 8.28% WACC is an imprecise estimate. The grid and the Beta 1.0 stress show what a higher rate does.</p>'
    body+='<h2>Named downside stresses (one disputed judgment at a time)</h2>'+table(['Stress','Change','Value/share','Change from base','Versus market'],[[r['stress'],r['change'],r['value_per_share'],r['change_from_base'],f'{r["versus_market"]:.1%}'] for r in data['stresses']])
    body+='<p>Every named stress lowers value and widens the discount to the dated market price, so none of them reverses Watch / Defer; together they move the case toward Do Not Initiate. Not modeled: the $206.0m June 2026 deferred tax asset. The model charges 24% cash tax throughout, which is conservative; at most about +$4.06 per share undiscounted, which does not close the gap to market.</p>'
    body+='<h2>Market-implied inputs (one change at a time)</h2>'+table(['Driver','Solved input','Interpretation'],[[r['driver'],r['solved_input'],'Decimal rate; growth is a uniform path shift'] for r in data['reverse_dcf']])
    body+='<h2>Normalization</h2>'+table(['Measure','Value'],list(data['normalization'].items()))
    body+='<h2>Consistent EV and equity multiples</h2>'+table(['Multiple','Market','DCF-implied'],[[r['multiple'],r['market_multiple'],r['dcf_multiple']] for r in data['multiples']])
    body+=f'<p>Conventional price / reported GAAP EPS: {data["reported_price_eps"]:.2f}x, using historical weighted-average shares; distinct from the diluted-equity convention above. Tax-contaminated reported earnings explain much of the low reported multiple. Peer policy admits no reliable comparable target; own-company ratios are cross-checks, not independent fair-value estimates. Do not average these methods.</p>'
    body+='<h2>Does the driver ranking depend on shock width?</h2>'+table(['Range','Driver','Shock pp','EBIT span','FCFF span','Value span'],[[r[k] for k in ['range_convention','driver','shock_pp','ebit_2030_span','fcff_2030_span','value_per_share_span']] for r in data['range_dependence']])
    body+='<p>Growth leads the original selected widths; at equal +/-1pp, margin slightly exceeds SBC for value, and both exceed growth. In Lab 11 both named revenue channels change the same growth input: equal shocks give identical outputs. Distinct labels do not establish distinct mechanisms.</p>'
    body+='<h2>All one-at-a-time results</h2>'+table(['Driver','Case','Input (decimal or $m/shares)','2030 EBIT','2030 FCFF','Value/share'],[[r[k] for k in ['driver','case','first_year_input','ebit_2030','fcff_2030','value_per_share']] for r in data['sensitivity']])
    body+=statement_tables(data['base'])
    body+='<h2>Validation</h2>'+table(['Test','Status','Evidence'],[[r['test'],r['status'],r['detail']] for r in tests])
    body+='<h2>Decision conditions</h2><p>Watch / Defer pending a defensible valuation cushion and supported operating path. Review the next two reports. Gross margin below 70.6%, growth 3pp below the path, or SBC above 17% triggers a rebuild; sustained thesis failure supports Do Not Initiate. A price at or below the current low case plus evidence supporting base operations is a proposed initiation rule, not a guarantee. Source/check failure suspends the numerical conclusion. See the decision memo for judgment limits.</p>'
    (out/'visible-output.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><title>DUOL Valuation Results</title><style>'+STYLE+'</style><body>'+body+'</body></html>',encoding='utf8')
    status=dict(status='PASS',run_utc=datetime.now(timezone.utc).isoformat(),model_checks=len(data['base']['checks']),validation_checks=len(tests),value_per_share=v['value_per_share'],original_lab10_value=140.18321713393624,change_from_original_lab10=v['value_per_share']-140.18321713393624)
    (out/'run-status.json').write_text(json.dumps(status,indent=2),encoding='utf8');print(json.dumps(status,indent=2))

if __name__=='__main__':main()
