"""Controlled corruptions and independent arithmetic audits."""
import copy
import json
import numpy as np
import pandas as pd
from .valuation import dcf
from .checks import run_model_checks
from .data_loader import RAW,TAGS,BS

def broken_tests(model,interim,a,h):
    outcomes=[]
    mutations=[('unlinked cash',lambda m:m.__setitem__('cash',m.cash+10)),
      ('asset corrupted',lambda m:m.__setitem__('ar',m.ar+5)),
      ('cash floor',lambda m:m.__setitem__('cash',m.cash*0+50)),
      ('NaN',lambda m:m.__setitem__('revenue',m.revenue*np.nan)),
      ('cash-flow corrupted',lambda m:m.__setitem__('period_cfo',m.period_cfo+1)),
      ('fixed-asset roll-forward',lambda m:m.__setitem__('period_da_ppe',m.period_da_ppe+1)),
      ('UFCF corrupted',lambda m:m.__setitem__('ufcf',m.ufcf+1))]
    for name,mutate in mutations:
        broken=model.copy(deep=True);mutate(broken)
        checks=run_model_checks(broken,interim,a,h)
        assert (checks.status=='FAIL').any()
        try:dcf(broken,interim,a,h)
        except ValueError as e:outcomes.append(dict(test=name,status='PASS',valuation_blocked=True,error=str(e)))
        else:raise AssertionError('Broken model valued: '+name)
    for name,key,value in [('terminal equals WACC','terminal_growth',a['wacc'][0]),('terminal exceeds WACC','terminal_growth',a['wacc'][0]+.01),('zero shares','diluted_shares',0.),('cash floor only; accounting still balances','minimum_cash',model.cash.max()+1)]:
        bad=copy.deepcopy(a);bad[key][:]=value
        try:dcf(model,interim,bad,h)
        except ValueError as e:outcomes.append(dict(test=name,status='PASS',valuation_blocked=True,error=str(e)))
        else:raise AssertionError('Invalid valuation inputs accepted')
    dcf(model,interim,a,h)
    return pd.DataFrame(outcomes)

def independent_audit(h,interim,model,a,v,discounts,shocks,implied,prices):
    checks=[]
    def record(name,ok,detail):
        checks.append(dict(check=name,status='PASS' if bool(ok) else 'FAIL',evidence=detail))
    filed={2023:dict(revenue=531.109,ebit=-13.259,net_income=16.067,assets=953.957,equity=655.501,cfo=153.614,capex=13.684),
           2024:dict(revenue=748.024,ebit=62.595,net_income=88.574,assets=1301.728,equity=824.550,cfo=285.513,capex=21.140),
           2025:dict(revenue=1037.589,ebit=135.570,net_income=414.065,assets=1992.182,equity=1347.006,cfo=387.823,capex=27.399)}
    for year,expected in filed.items():
        for key,val in expected.items():record(f'SEC cross-check {year} {key}',abs(h.loc[year,key]-val)<.00001,'10-K statement cross-check, USD millions')
    inline=json.loads((RAW/'annual_inline_xbrl.json').read_text())['facts']
    for year in h.index:
        for key,tag in TAGS.items():
            if key=='other_net':continue # computed statement subtotal, not generic nonoperating tag
            candidates=[x['value_millions'] for x in inline if x['tag']=='us-gaap:'+tag and x['end']==f'{year}-12-31' and x['start']==('' if key in BS else f'{year}-01-01') and not x['dimensional']]
            if candidates:record(f'Inline filing/API agreement {year} {key}',any(abs(h.loc[year,key]-x)<.00001 for x in candidates),'Separately parsed original annual HTML vs SEC companyfacts; matched dates and non-dimensional context')
    for key,val in dict(revenue=590.421,ebit=78.472,cash=1180.887,assets=2073.953,equity=1409.742,cfo=239.031,capex=12.615,sbc=72.857,da=8.438).items():
        record('Interim filing cross-check '+key,abs(interim[key]-val)<1e-8,'Q2 2026 10-Q and letter financial statements')
    nasdaq=json.loads((RAW/'nasdaq-price.json').read_text())['data']['tradesTable']['rows']
    record('Independent market close',next(x['close'] for x in nasdaq if x['date']=='09/21/2026')=='$149.42','Nasdaq close independently matches Yahoo149.42')
    record('Dates and units',list(h.index)==[2023,2024,2025] and list(model.index)==list(range(2026,2031)),'Fiscal years; SEC USD / 1e6; shares / 1e6; rates decimal')
    record('Guidance revenue',abs(model.iloc[0].revenue-1207)<1e-8,'Q2 letter $1,207m FY2026 guidance')
    record('Guidance gross margin',abs(model.iloc[0].gross_profit/model.iloc[0].revenue-.716)<1e-8,'Q2 letter 71.6%')
    record('Guidance SBC',abs(model.iloc[0].sbc/model.iloc[0].revenue-.15)<1e-8,'Q2 letter approximately 15%')
    record('All scenarios executed',len(shocks)==len(a) and shocks.status.eq('ALL CHECKS PASS').all(),'Each scenario reconstructs statements and invokes the same gated DCF')
    record('Reverse price residuals',implied.loc[implied.market_implied.notna(),'residual'].abs().max()<1e-6,'Brent roots; invalid states excluded; no interpolated answer')
    record('Beta observations',len(prices)==61 and len(prices.pct_change().dropna())==60,'Aug2021–Aug2026; DUOL IPO July2021; no fabricated prices')
    record('PV independent arithmetic',abs(sum(discounts.future_ufcf/(1+v['wacc'])**discounts.discount_period)-v['pv_explicit'])<1e-8,'Independent vector calculation')
    record('Terminal independent arithmetic',abs(v['terminal_fcf']/(v['wacc']-v['terminal_growth'])-v['terminal_value'])<1e-8,'Positive denominator and recomputed terminal cash flow')
    record('Bridge independent arithmetic',abs(v['enterprise_value']+v['excess_cash']-v['equity_value'])<1e-8,'Cash + all investments less $100m reserve; zero traditional debt')
    record('Per share independent arithmetic',abs(v['equity_value']/v['diluted_shares']-v['value_per_share'])<1e-10,'50.7m company estimated diluted shares')
    record('SBC economic expense',all(abs(y.ufcf-(y.nopat+y.period_da-y.period_capex-y.delta_nwc))<1e-8 for _,y in model.iterrows()),'CFO adds SBC; FCFF does not. No annual dilution multiplier.')
    record('Partial year timing',0<discounts.discount_period.iloc[0]<1 and discounts.future_ufcf.iloc[0]==model.ufcf.iloc[0]*v['remaining_h2_fraction'],'Only remaining H2 enters DCF; ACT/365 end-year discounting')
    audit=pd.DataFrame(checks)
    if not audit.status.eq('PASS').all():raise AssertionError(audit[audit.status!='PASS'].to_string())
    return audit
