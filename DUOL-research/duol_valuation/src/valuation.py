import numpy as np
import pandas as pd
from .checks import run_model_checks,require_pass
from .data_loader import ASOF

def dcf(model,interim,a,history=None):
    require_pass(run_model_checks(model,interim,a,history))
    r=float(a['wacc'][0]);g=float(a['terminal_growth'][0]);shares=float(a['diluted_shares'][0])
    date=pd.Timestamp(ASOF);start=pd.Timestamp('2026-06-30');end=pd.Timestamp('2026-12-31')
    elapsed=(date-start).days/(end-start).days
    cashflows=model.ufcf.to_numpy().copy();cashflows[0]*=(1-elapsed)
    periods=np.array([(pd.Timestamp(f'{y}-12-31')-date).days/365 for y in model.index])
    discount=(1+r)**(-periods);pv=cashflows*discount
    last=model.iloc[-1];next_revenue=last.revenue*(1+g)
    terminal_ebit=next_revenue*last.operating_margin
    terminal_nopat=terminal_ebit-max(0.,terminal_ebit)*a['tax_rate'][-1]
    terminal_da=next_revenue*a['da_ratio'][-1];terminal_capex=next_revenue*a['capex_ratio'][-1]
    terminal_delta_nwc=last.nwc*g
    terminal_reinvestment=terminal_capex-terminal_da+terminal_delta_nwc
    terminal_fcf=terminal_nopat-terminal_reinvestment
    if not np.isfinite(terminal_fcf) or terminal_fcf<=0:raise ValueError('MODEL CHECK FAILED — VALUATION DISABLED: non-positive/invalid terminal cash flow')
    tv=terminal_fcf/(r-g);pvtv=tv*discount[-1];ev=float(pv.sum()+pvtv)
    # Reported June liquidity rolled to valuation date using economic (SBC-expensed)
    # operating cash generation plus after-tax interest. This is an estimate, not a filed balance.
    first=model.iloc[0]
    interim_to_date=elapsed*(first.ufcf+first.period_interest_income*(1-a['tax_rate'][0]))
    known_post_h1_buyback=71.9-69.603 # Aug1 cumulative rounded disclosure less H1 cash repurchases
    liquidity=interim['cash']+interim['investments']+interim_to_date-known_post_h1_buyback
    excess=liquidity-a['minimum_cash'][0]
    equity=ev+excess # debt zero, operating lease charges already in EBIT; no lease subtraction
    out=dict(enterprise_value=ev,equity_value=float(equity),value_per_share=float(equity/shares),pv_explicit=float(pv.sum()),
      terminal_value=float(tv),pv_terminal=float(pvtv),terminal_share_ev=float(pvtv/ev),terminal_fcf=float(terminal_fcf),
      terminal_growth=g,wacc=r,diluted_shares=shares,reported_cash=interim['cash'],reported_investments=interim['investments'],
      estimated_elapsed_cash=float(interim_to_date),post_h1_buyback=known_post_h1_buyback,minimum_cash=float(a['minimum_cash'][0]),
      excess_cash=float(excess),debt=0.,lease_adjustment=0.,terminal_revenue=float(next_revenue),terminal_ebit=float(terminal_ebit),
      terminal_da=float(terminal_da),terminal_capex=float(terminal_capex),terminal_delta_nwc=float(terminal_delta_nwc),
      terminal_reinvestment=float(terminal_reinvestment),terminal_ev_revenue=float(tv/next_revenue),
      terminal_ev_ebitda=float(tv/(terminal_ebit+terminal_da)),terminal_implied_roic=float(g*terminal_nopat/terminal_reinvestment) if terminal_reinvestment>0 else None,
      remaining_h2_fraction=1-elapsed,valuation_date=ASOF)
    if not all(np.isfinite(v) for v in out.values() if isinstance(v,(float,int))):raise ValueError('Non-finite valuation')
    table=pd.DataFrame({'year':model.index,'future_ufcf':cashflows,'discount_period':periods,'discount_factor':discount,'pv_ufcf':pv})
    return out,table
