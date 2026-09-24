import copy
import numpy as np
import pandas as pd
from .forecast import project
from .valuation import dcf

def rerun(h,interim,a,changes=None):
    changed=copy.deepcopy(a)
    for k,v in (changes or {}).items():changed[k]=np.full(5,v,dtype=float) if np.isscalar(v) else np.asarray(v,dtype=float)
    model=project(h,interim,changed)
    return dcf(model,interim,changed,h)[0],model,changed

def sensitivities(h,interim,a,assumptions):
    base,_,_=rerun(h,interim,a);rows=[]
    for key,group in assumptions.groupby('assumption_name',sort=False):
        lo=group.downside_value.to_numpy().copy();hi=group.upside_value.to_numpy().copy()
        if key in ['buybacks','option_proceeds']:lo=np.maximum(lo,0)
        low=rerun(h,interim,a,{key:lo})[0]['value_per_share'];high=rerun(h,interim,a,{key:hi})[0]['value_per_share']
        down=min(low,high);up=max(low,high)
        rows.append(dict(assumption=key,parameter_low=lo.tolist(),parameter_high=hi.tolist(),low_parameter_price=low,high_parameter_price=high,
          downside=down,base=base['value_per_share'],upside=up,down_change=down-base['value_per_share'],up_change=up-base['value_per_share'],
          absolute_sensitivity=up-down,percentage_sensitivity=(up-down)/base['value_per_share'],status='ALL CHECKS PASS'))
    shocks=pd.DataFrame(rows).sort_values('absolute_sensitivity',ascending=False)
    rates=[]
    for r in a['wacc'][0]+np.arange(-3,4)*.01:
        v,_,_=rerun(h,interim,a,{'wacc':r});rates.append({k:v[k] for k in ['wacc','enterprise_value','equity_value','value_per_share','terminal_share_ev']})
    cases=[]
    changes={'Bear':{'growth':a['growth']-.03,'gross_margin':a['gross_margin']-.01,'rd_ex_sbc':a['rd_ex_sbc']+.01},
             'Base':{},'Bull':{'growth':a['growth']+.03,'gross_margin':a['gross_margin']+.01,'rd_ex_sbc':a['rd_ex_sbc']-.01}}
    for name,ch in changes.items():
        v,m,_=rerun(h,interim,a,ch);cases.append(dict(case=name,value_per_share=v['value_per_share'],terminal_share_ev=v['terminal_share_ev'],minimum_forecast_cash=m.cash.min(),check_status='PASS'))
    additive=base['value_per_share']+sum(rerun(h,interim,a,{k:v})[0]['value_per_share']-base['value_per_share'] for k,v in changes['Bear'].items())
    cases.append(dict(case='Incorrect sum of isolated bear shocks',value_per_share=additive,terminal_share_ev=None,minimum_forecast_cash=None,check_status='NOT A MODEL RERUN'))
    grid=[]
    for g in [.02,.025,.03,.035,.04]:
        for r in a['wacc'][0]+np.arange(-3,4)*.01:
            v,_,_=rerun(h,interim,a,{'terminal_growth':g,'wacc':r});grid.append(dict(terminal_growth=g,wacc=r,value_per_share=v['value_per_share']))
    return shocks,pd.DataFrame(rates),pd.DataFrame(cases),pd.DataFrame(grid)
