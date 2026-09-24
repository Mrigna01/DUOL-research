import numpy as np
import pandas as pd
from scipy.optimize import brentq
from .sensitivity import rerun

def solve_implied(h,interim,a,price):
    specs=[('WACC',a['wacc'][0],.041,.30,lambda x:{'wacc':x}),
           ('Terminal growth',a['terminal_growth'][0],-.03,min(.06,a['wacc'][0]-.001),lambda x:{'terminal_growth':x}),
           ('Revenue growth path shift',0.,-.10,.15,lambda x:{'growth':a['growth']+x}),
           ('Operating margin path shift',0.,-.06,.10,lambda x:{'ga_ex_sbc':a['ga_ex_sbc']-x}),
           ('Gross margin path shift',0.,-.08,.15,lambda x:{'gross_margin':a['gross_margin']+x}),
           ('Capex / revenue',a['capex_ratio'][0],.005,.12,lambda x:{'capex_ratio':x})]
    records=[]
    for name,base,lo,hi,changes in specs:
        f=lambda x:rerun(h,interim,a,changes(x))[0]['value_per_share']-price
        samples=[]
        for x in np.linspace(lo,hi,101):
            try:samples.append((x,f(x)))
            except ValueError:samples.append((x,None))
        bracket=next(((x,z) for (x,y),(z,w) in zip(samples,samples[1:]) if y is not None and w is not None and y*w<=0),None)
        if bracket is None:
            records.append(dict(variable=name,base_case=base,market_implied=None,residual=None,status='NO FEASIBLE ROOT IN STATED BRACKET',search_low=lo,search_high=hi))
            continue
        root=brentq(f,*bracket,xtol=1e-12);res=f(root)
        if abs(res)>1e-6:raise AssertionError('Reverse DCF residual exceeds tolerance')
        records.append(dict(variable=name,base_case=base,market_implied=root,residual=res,status='SOLVED; FULL MODEL CHECKS PASS',search_low=lo,search_high=hi))
    return pd.DataFrame(records)
