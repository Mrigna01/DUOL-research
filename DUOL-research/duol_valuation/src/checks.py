"""Checks recompute identities from constituent lines, not cached totals alone."""
import numpy as np
import pandas as pd
from .forecast import ASSET_KEYS,LIABILITY_KEYS

def run_model_checks(model,interim,a,history=None):
    rows=[];tol=1e-7
    def check(name,year,value,passed,notes='',tolerance=tol):
        rows.append(dict(check_name=name,year=year,value=value,tolerance=tolerance,status='PASS' if passed else 'FAIL',notes=notes))
    if history is not None:
        for year,y in history.iterrows():
            for name,gap in [('Historical balance',y.assets-y.liabilities-y.equity),('Historical gross profit',y.revenue-y.cost_of_revenue-y.gross_profit),('Historical EBIT',y.gross_profit-y.rd-y.sm-y.ga-y.ebit),('Historical net income',y.pretax-y.tax-y.net_income)]:
                check(name,year,gap,abs(gap)<.005,'USD millions',.005)
            for name,gap in [('Historical assets sum',sum(y[k] for k in ASSET_KEYS)-y.assets),('Historical liabilities sum',sum(y[k] for k in LIABILITY_KEYS)-y.liabilities)]:
                check(name,year,gap,abs(gap)<.005,tolerance=.005)
            if year>history.index.min():
                gap=y.cash-history.loc[year-1,'cash']-y.cfo-y.cfi-y.cff
                check('Historical cash bridge',year,gap,abs(gap)<.005,tolerance=.005)
    prev=interim
    for i,(year,y) in enumerate(model.iterrows()):
        gaps={
          'Balance sheet':sum(y[k] for k in ASSET_KEYS)-sum(y[k] for k in LIABILITY_KEYS)-y.equity,
          'Assets total':sum(y[k] for k in ASSET_KEYS)-y.assets,
          'Liabilities total':sum(y[k] for k in LIABILITY_KEYS)-y.liabilities,
          'Cash reconciliation':y.cash-prev['cash']-y.period_cfo-y.period_cfi-y.period_cff,
          'PPE roll-forward':y.ppe-prev['ppe']-y.period_capex_ppe+y.period_da_ppe,
          'Intangibles roll-forward':y.intangibles-prev['intangibles']-y.period_capex_software+y.period_da_intangibles,
          'Equity roll-forward':y.equity-prev['equity']-y.period_net_income-y.period_sbc-y.period_cff,
          'Income statement':y.revenue-y.cost_of_revenue-y.rd-y.sm-y.ga-y.ebit,
          'CFO construction':y.period_cfo-y.period_net_income-y.period_da-y.period_sbc+y.delta_nwc,
          'UFCF construction':y.ufcf-(y.period_ebit-max(0.,y.period_ebit)*a['tax_rate'][i]+y.period_da-y.period_capex-y.delta_nwc),
          'NWC roll-forward':y.nwc-prev['nwc']-y.delta_nwc,
          'Debt roll-forward':y.debt-prev.get('debt',0)-y.financing_draw}
        for name,gap in gaps.items():check(name,year,gap,np.isfinite(gap) and abs(gap)<=tol)
        check('Minimum cash',year,y.cash-a['minimum_cash'][i],y.cash>=a['minimum_cash'][i]-tol,'No assumed financing plug')
        finite=np.isfinite(y.to_numpy(dtype=float)).all();check('No invalid values',year,int(finite),finite)
        keys=ASSET_KEYS+LIABILITY_KEYS+['revenue','period_revenue','period_da','period_capex','period_sbc','period_rd','period_sm','period_ga']
        minimum=min(y[k] for k in keys);check('Economically valid balances',year,minimum,minimum>=-tol,'Losses and negative working capital are allowed')
        prev=y
    for key,values in a.items():
        passed=np.isfinite(values).all()
        if key.endswith('_ratio') or key.endswith('_ex_sbc') or key in ['gross_margin','tax_rate','ppe_capex_share']:passed=passed and np.all((values>=0)&(values<=1))
        if key in ['diluted_shares','minimum_cash']:passed=passed and np.all(values>0)
        if key=='growth':passed=passed and np.all(values> -1)
        check('Valid assumption: '+key,'all',int(passed),passed)
    spread=float(a['wacc'][0]-a['terminal_growth'][0]);check('WACC > terminal growth','terminal',spread,spread>0 and a['wacc'][0]>0 and a['terminal_growth'][0]>-1)
    return pd.DataFrame(rows)

def require_pass(checks):
    failures=checks.loc[checks.status!='PASS']
    if len(failures):
        raise ValueError('MODEL CHECK FAILED — VALUATION DISABLED: '+ '; '.join(f"{r.check_name} ({r.year}): {r.value}" for r in failures.itertuples()))

def display_checks(checks):
    require_pass(checks)
    print('FINAL MODEL CHECKS\n'+'='*64)
    print(checks.groupby('check_name',sort=False).status.first().to_string())
    print('='*64+f'\nALL {len(checks)} REQUIRED CHECKS PASSED\nVALUATION ENABLED')
