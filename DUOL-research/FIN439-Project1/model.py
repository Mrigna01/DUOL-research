"""DUOL five-year operating model and FCFF valuation.
All amounts USD millions except rates and per-share value. Standard library only.
Model development and source history: docs/research-evolution.md.
"""
from pathlib import Path
import csv, math, copy
from datetime import date
from statistics import covariance, variance, correlation
ROOT=Path(__file__).resolve().parent
ASOF=date(2026,9,21)
PRICE=149.42
ASSETS=['cash','short_investments','long_investments','ar','deferred_cost','prepaid','tax_receivable','ppe','intangibles','rou','goodwill','restricted_cash','dta','other_assets']
LIABILITIES=['ap','accrued','deferred_revenue','tax_payable','lease_noncurrent','dtl','other_liabilities']
FLOWS=['revenue','cost_of_revenue','gross_profit','rd','sm','ga','opex','ebit','interest_income','other_net','pretax','tax','net_income','sbc','da','capex','capex_ppe','capex_software','cfo','cfi','cff']

def load_data():
    with (ROOT/'data/historical_financials.csv').open(encoding='utf8') as f:
        h={int(r['year']):{k:float(v) for k,v in r.items()} for r in csv.DictReader(f)}
    with (ROOT/'data/h1_2026.csv').open(encoding='utf8') as f:
        reader=csv.reader(f);next(reader);interim={k:float(v) for k,v in reader}
    return h,interim

def wacc_evidence():
    with (ROOT/'data/monthly_prices.csv').open(encoding='utf8') as f:prices=list(csv.DictReader(f))
    returns={k:[float(b[k])/float(a[k])-1 for a,b in zip(prices,prices[1:])] for k in ['DUOL','SPY']}
    beta=covariance(returns['DUOL'],returns['SPY'])/variance(returns['SPY'])
    # Reliability diagnostics only; they do not change the selected WACC.
    n=len(returns['DUOL']);rho=correlation(returns['DUOL'],returns['SPY'])
    x=returns['SPY'];y=returns['DUOL'];mx=sum(x)/n;my=sum(y)/n
    residuals=[yy-my-beta*(xx-mx) for xx,yy in zip(x,y)]
    se=math.sqrt(sum(e*e for e in residuals)/(n-2)/sum((xx-mx)**2 for xx in x))
    total=[[float(b[k])/float(a[k])-1 for a,b in zip(prices,prices[1:])] for k in ['DUOL_adjusted','SPY_adjusted']]
    return dict(beta=beta,risk_free=.0475,equity_risk_premium=.0414,debt_weight=0.,wacc=.0475+beta*.0414,observations=n,period_start=prices[0][''],period_end=prices[-1][''],rate_vintage='2026-09-01',definition='Unadjusted monthly close returns; covariance/variance; zero financial debt',r_squared=rho**2,beta_standard_error=se,beta_ci95_low=beta-1.96*se,beta_ci95_high=beta+1.96*se,total_return_beta=covariance(*total)/variance(total[1]))

def assumptions():
    with (ROOT/'data/assumptions.csv').open(encoding='utf8') as f:records=list(csv.DictReader(f))
    a={}
    for r in records:a.setdefault(r['assumption_name'],[]).append(float(r['base_value']))
    calculated=wacc_evidence()['wacc']
    if abs(a['wacc'][0]-calculated)>1e-10:raise ValueError('WACC source calculation differs from assumption ledger')
    return a

def liquidity_inputs():
    with (ROOT/'data/liquidity_bridge.csv').open(encoding='utf8') as f:
        return {r['input']:float(r['value_m']) for r in csv.DictReader(f)}

def forecast(h,interim,a):
    previous=dict(interim);prior_revenue=h[2025]['revenue'];rows=[]
    bridge=liquidity_inputs()
    # Financing payable is included in reported current liabilities, not operating NWC.
    previous['nwc']+=bridge['h1_unsettled_repurchases']
    for i in range(5):
        v=lambda k:a[k][i]
        actual=interim if i==0 else {k:0. for k in FLOWS}
        y={k:previous[k] for k in ASSETS+LIABILITIES};y['year']=2026+i
        revenue=prior_revenue*(1+v('growth'))
        target={'revenue':revenue,'gross_profit':revenue*v('gross_margin'),'sbc':revenue*v('sbc_ratio'),'da':revenue*v('da_ratio'),'capex':revenue*v('capex_ratio')}
        # Presentation allocation only: all SBC remains an economic cost in EBIT/FCFF.
        for key,weight in [('rd',.7),('sm',.1),('ga',.2)]:target[key]=revenue*v(key+'_ex_sbc')+weight*target['sbc']
        for key,value in target.items():y['period_'+key]=value-actual[key]
        y['period_cost_of_revenue']=y['period_revenue']-y['period_gross_profit']
        y['period_opex']=sum(y['period_'+k] for k in ['rd','sm','ga'])
        y['period_ebit']=y['period_gross_profit']-y['period_opex']
        fraction=184/365 if i==0 else 1.
        y['period_interest_income']=(previous['cash']+previous['short_investments']+previous['long_investments'])*v('investment_yield')*fraction
        y['period_other_net']=0.
        y['period_pretax']=y['period_ebit']+y['period_interest_income']
        y['period_tax']=max(0.,y['period_pretax'])*v('tax_rate')
        y['period_net_income']=y['period_pretax']-y['period_tax']
        for k in ['ar','deferred_cost','prepaid','ap','accrued','deferred_revenue']:y[k]=revenue*v(k+'_ratio')
        y['nwc']=sum(y[k] for k in ['ar','deferred_cost','prepaid'])-sum(y[k] for k in ['ap','accrued','deferred_revenue'])
        y['delta_nwc']=y['nwc']-previous['nwc']
        y['period_capex_ppe']=y['period_capex']*v('ppe_capex_share')
        y['period_capex_software']=y['period_capex']-y['period_capex_ppe']
        y['period_da_ppe']=y['period_da']*previous['ppe']/(previous['ppe']+previous['intangibles'])
        y['period_da_intangibles']=y['period_da']-y['period_da_ppe']
        y['ppe']=previous['ppe']+y['period_capex_ppe']-y['period_da_ppe']
        y['intangibles']=previous['intangibles']+y['period_capex_software']-y['period_da_intangibles']
        y['period_cfo']=y['period_net_income']+y['period_da']+y['period_sbc']-y['delta_nwc']
        y['period_cfi']=-y['period_capex']
        y['period_withholding']=y['period_sbc']*v('withholding_ratio')
        y['period_buybacks']=v('buybacks')*fraction+(bridge['repurchases_through_aug1']-bridge['h1_recognized_repurchases'] if i==0 else 0.)
        y['period_repurchase_settlement']=bridge['h1_unsettled_repurchases'] if i==0 else 0.
        y['period_option_proceeds']=max(0.,v('option_proceeds'))*fraction
        y['period_cff']=y['period_option_proceeds']-y['period_withholding']-y['period_buybacks']-y['period_repurchase_settlement']
        y['equity']=previous['equity']+y['period_net_income']+y['period_sbc']+y['period_cff']+y['period_repurchase_settlement']
        y['cash']=previous['cash']+y['period_cfo']+y['period_cfi']+y['period_cff']
        y['assets']=sum(y[k] for k in ASSETS);y['liabilities']=sum(y[k] for k in LIABILITIES)
        y['fcff']=y['period_ebit']-max(0.,y['period_ebit'])*v('tax_rate')+y['period_da']-y['period_capex']-y['delta_nwc']
        h1_fcff=interim['ebit']*(1-v('tax_rate'))+interim['da']-interim['capex']-(interim['nwc']+bridge['h1_unsettled_repurchases']-h[2025]['nwc']) if i==0 else 0.
        y['annual_fcff']=y['fcff']+h1_fcff
        for k in FLOWS:y[k]=y['period_'+k]+actual[k]
        y['operating_margin']=y['ebit']/y['revenue'];rows.append(y);previous=y;prior_revenue=revenue
    return rows

def checks(rows,h,interim,a):
    out=[]
    def record(name,year,gap,limit=1e-7):out.append(dict(test=name,year=year,gap=gap,status='PASS' if math.isfinite(gap) and abs(gap)<=limit else 'FAIL'))
    previous=None
    for year,y in list(h.items())+[(2026,interim)]:
        for name,gap in [('Historical balance',y['assets']-y['liabilities']-y['equity']),('Historical assets',sum(y[k] for k in ASSETS)-y['assets']),('Historical liabilities',sum(y[k] for k in LIABILITIES)-y['liabilities']),('Historical EBIT',y['gross_profit']-y['rd']-y['sm']-y['ga']-y['ebit']),('Historical net income',y['pretax']-y['tax']-y['net_income'])]:record(name,year,gap,.005)
        if previous:record('Historical cash flow',year,y['cash']-previous['cash']-y['cfo']-y['cfi']-y['cff'],.005)
        previous=y
    previous=dict(interim);previous['nwc']+=liquidity_inputs()['h1_unsettled_repurchases']
    for i,y in enumerate(rows):
        gaps={
            'Balance sheet':sum(y[k] for k in ASSETS)-sum(y[k] for k in LIABILITIES)-y['equity'],
            'Assets total':sum(y[k] for k in ASSETS)-y['assets'],
            'Liabilities total':sum(y[k] for k in LIABILITIES)-y['liabilities'],
            'Period cash bridge':y['cash']-previous['cash']-y['period_cfo']-y['period_cfi']-y['period_cff'],
            'Annual cash bridge':y['cash']-(h[2025]['cash'] if i==0 else previous['cash'])-y['cfo']-y['cfi']-y['cff'],
            'CFO identity':y['period_cfo']-y['period_net_income']-y['period_da']-y['period_sbc']+y['delta_nwc'],
            'FCFF identity':y['fcff']-(y['period_ebit']-max(0.,y['period_ebit'])*a['tax_rate'][i]+y['period_da']-y['period_capex']-y['delta_nwc']),
            'NWC identity':y['nwc']-sum(y[k] for k in ['ar','deferred_cost','prepaid'])+sum(y[k] for k in ['ap','accrued','deferred_revenue']),
            'NWC change':y['nwc']-previous['nwc']-y['delta_nwc'],
            'PPE roll-forward':y['ppe']-previous['ppe']-y['period_capex_ppe']+y['period_da_ppe'],
            'Software roll-forward':y['intangibles']-previous['intangibles']-y['period_capex_software']+y['period_da_intangibles'],
            'Equity roll-forward':y['equity']-previous['equity']-y['period_net_income']-y['period_sbc']-y['period_cff']-y['period_repurchase_settlement'],
            'FCFF to statement cash':y['fcff']-(y['period_cfo']-y['period_sbc']-y['period_capex']-y['period_interest_income']-y['period_other_net']+y['period_tax']-max(0.,y['period_ebit'])*a['tax_rate'][i]),
            'Financing cash flow':y['period_cff']-y['period_option_proceeds']+y['period_withholding']+y['period_buybacks']+y['period_repurchase_settlement'],
            'Pretax income':y['pretax']-y['ebit']-y['interest_income']-y['other_net'],
            'Operating income':y['revenue']-y['cost_of_revenue']-y['rd']-y['sm']-y['ga']-y['ebit'],
            'Net income':y['pretax']-y['tax']-y['net_income']}
        for name,gap in gaps.items():record(name,y['year'],gap)
        record('Finite lines',y['year'],0 if all(math.isfinite(x) for x in y.values()) else 1)
        record('Cash floor',y['year'],min(0.,y['cash']-a['minimum_cash'][i]))
        record('Nonnegative balances',y['year'],min(0.,*(y[k] for k in ASSETS+LIABILITIES+['period_revenue','period_capex','period_da','period_sbc'])))
        previous=y
    for k,values in a.items():
        valid=len(values)==5 and all(math.isfinite(x) for x in values)
        if k.endswith(('_ratio','_ex_sbc')) or k in ['gross_margin','tax_rate','ppe_capex_share']:valid=valid and all(0<=x<=1 for x in values)
        if k in ['diluted_shares','minimum_cash']:valid=valid and all(x>0 for x in values)
        if k=='growth':valid=valid and all(x>-1 for x in values)
        record('Assumption '+k,'all',0 if valid else 1)
    record('WACC > g','terminal',0 if a['wacc'][0]>max(0.,a['terminal_growth'][0]) and a['terminal_growth'][0]>-1 else 1)
    return out

def require_pass(check_rows):
    failed=[r for r in check_rows if r['status']!='PASS']
    if failed:raise ValueError('VALUATION BLOCKED: '+ '; '.join(f"{r['test']} ({r['year']}): {r['gap']}" for r in failed))

def valuation(rows,h,interim,a):
    require_pass(checks(rows,h,interim,a))
    r=a['wacc'][0];g=a['terminal_growth'][0];shares=a['diluted_shares'][0]
    elapsed=(ASOF-date(2026,6,30)).days/184
    discounted=[]
    for i,y in enumerate(rows):
        t=(date(y['year'],12,31)-ASOF).days/365
        cash=y['fcff']*(1-elapsed if i==0 else 1)
        discounted.append(dict(year=y['year'],future_fcff=cash,period=t,pv=cash/(1+r)**t))
    last=rows[-1];terminal_revenue=last['revenue']*(1+g)
    terminal_nopat=terminal_revenue*last['operating_margin']*(1-a['tax_rate'][-1])
    reinvestment=terminal_revenue*(a['capex_ratio'][-1]-a['da_ratio'][-1])+last['nwc']*g
    terminal_fcff=terminal_nopat-reinvestment
    if not math.isfinite(terminal_fcff) or terminal_fcff<=0:raise ValueError('VALUATION BLOCKED: terminal FCFF must be positive')
    tv=terminal_fcff/(r-g);pv_tv=tv/(1+r)**discounted[-1]['period'];pv_explicit=sum(x['pv'] for x in discounted)
    ev=pv_explicit+pv_tv
    bridge=liquidity_inputs()
    new_repurchases=bridge['repurchases_through_aug1']-bridge['h1_recognized_repurchases']
    settlement=bridge['h1_unsettled_repurchases']
    known_payments=new_repurchases+settlement
    first=rows[0]
    # Known repurchases are assumed settled by the valuation date; prorate other H2 flows.
    elapsed_cash=elapsed*(first['period_cfo']+first['period_cfi']+first['period_cff']+known_payments)
    dated_cash=interim['cash']+elapsed_cash-known_payments
    excess=dated_cash+interim['investments']-a['minimum_cash'][0]
    equity=ev+excess
    return dict(valuation_date=ASOF.isoformat(),market_price=PRICE,enterprise_value=ev,equity_value=equity,value_per_share=equity/shares,pv_explicit=pv_explicit,terminal_value=tv,pv_terminal=pv_tv,terminal_share=pv_tv/ev,wacc=r,terminal_growth=g,diluted_shares=shares,reported_cash=interim['cash'],investments=interim['investments'],estimated_elapsed_cash=elapsed_cash,post_h1_buybacks=known_payments,new_post_h1_repurchases=new_repurchases,settlement_of_h1_repurchases=settlement,estimated_dated_cash=dated_cash,minimum_cash=a['minimum_cash'][0],excess_cash=excess,debt=0.,terminal_fcff=terminal_fcff,terminal_reinvestment=reinvestment,terminal_roic=g*terminal_nopat/reinvestment if reinvestment>0 else None,terminal_roic20_value=(pv_explicit+terminal_nopat*(1-g/.20)/(r-g)/(1+r)**discounted[-1]['period']+excess)/shares,discounted=discounted)

def run(overrides=None):
    h,interim=load_data();a=assumptions()
    for k,v in (overrides or {}).items():
        if k not in a:raise ValueError('Unknown assumption: '+k)
        a[k]=list(v) if isinstance(v,(list,tuple)) else [v]*5
    for k,values in a.items():
        if len(values)!=5 or any(isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x) for x in values):
            raise ValueError('VALUATION BLOCKED: '+k+' requires five finite numeric inputs')
        if (k.endswith(('_ratio','_ex_sbc')) or k in ['gross_margin','tax_rate','ppe_capex_share']) and any(not 0<=x<=1 for x in values):
            raise ValueError('VALUATION BLOCKED: '+k+' must be between zero and one')
        if k in ['wacc','terminal_growth','diluted_shares'] and len(set(values))!=1:
            raise ValueError('VALUATION BLOCKED: '+k+' is one valuation-date input, not an annual path')
        if k in ['buybacks','option_proceeds','investment_yield'] and any(x<0 for x in values):
            raise ValueError('VALUATION BLOCKED: '+k+' cannot be negative')
    rows=forecast(h,interim,a);c=checks(rows,h,interim,a);require_pass(c)
    return dict(statements=rows,valuation=valuation(rows,h,interim,a),checks=c,assumptions=a)

if __name__=='__main__':
    import json
    print(json.dumps(run()['valuation'],indent=2))
