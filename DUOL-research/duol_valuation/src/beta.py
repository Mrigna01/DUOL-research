import numpy as np
import pandas as pd
from scipy.stats import linregress,t

def estimate(prices):
    returns=prices.pct_change(fill_method=None).iloc[1:]
    records=[]
    for suffix,label in [('', 'Course: unadjusted monthly closes'),('_adjusted','Robustness: adjusted monthly closes')]:
        x=returns['SPY'+suffix]; y=returns['DUOL'+suffix]; r=linregress(x,y)
        cov_beta=np.cov(x,y,ddof=1)[0,1]/np.var(x,ddof=1)
        assert abs(cov_beta-r.slope)<1e-12
        ci=t.ppf(.975,len(x)-2)*r.stderr
        records.append(dict(method=label,price_start=str(prices.index[0]),price_end=str(prices.index[-1]),price_count=len(prices),return_count=len(x),
          beta=r.slope,blume_beta=.67*r.slope+.33,alpha_monthly=r.intercept,r_squared=r.rvalue**2,correlation=r.rvalue,
          standard_error=r.stderr,p_value=r.pvalue,ci95_low=r.slope-ci,ci95_high=r.slope+ci,
          duol_mean=y.mean(),spy_mean=x.mean(),duol_vol=y.std(),spy_vol=x.std()))
    return pd.DataFrame(records),returns
