import json
from pathlib import Path
import pandas as pd
from .data_loader import ROOT,load_data,price_data,ASOF
from .historical_analysis import analyze
from .beta import estimate
from .assumptions import build_assumptions,unpack
from .forecast import project,ASSET_KEYS,LIABILITY_KEYS
from .checks import run_model_checks,require_pass
from .valuation import dcf
from .sensitivity import sensitivities,rerun
from .implied_expectations import solve_implied
from .validation import broken_tests,independent_audit
from .abg_validation import validate_abg
from .charts import make_charts

IS=['revenue','cost_of_revenue','gross_profit','rd','sm','ga','opex','ebit','interest_income','other_net','pretax','tax','net_income','sbc','da']
BS=ASSET_KEYS+['assets']+LIABILITY_KEYS+['liabilities','equity']
CF=['cfo','capex_ppe','capex_software','cfi','cff','cash','period_cfo','period_cfi','period_cff','period_sbc','period_withholding','period_buybacks','period_option_proceeds']

def terminal_variants(v,m,a):
    last=m.iloc[-1];r=v['wacc'];g=v['terminal_growth'];factor=v['pv_terminal']/v['terminal_value'];rows=[]
    for label,reinvest in [('Base: operating balance drivers',v['terminal_reinvestment']),('Steady-state 20% incremental ROIC',v['terminal_ebit']*(1-a['tax_rate'][-1])*g/.20),('Steady-state 30% incremental ROIC',v['terminal_ebit']*(1-a['tax_rate'][-1])*g/.30)]:
        cf=v['terminal_ebit']*(1-a['tax_rate'][-1])-reinvest
        value=(v['pv_explicit']+cf/(r-g)*factor+v['excess_cash'])/v['diluted_shares']
        rows.append(dict(convention=label,terminal_reinvestment=reinvest,terminal_fcf=cf,value_per_share=value))
    naive=last.ufcf*(1+g)
    rows.append(dict(convention='Mechanical final-year FCF growth (diagnostic)',terminal_reinvestment=None,terminal_fcf=naive,value_per_share=(v['pv_explicit']+naive/(r-g)*factor+v['excess_cash'])/v['diluted_shares']))
    return pd.DataFrame(rows)

def run_analysis():
    tables=ROOT/'outputs/tables';tables.mkdir(parents=True,exist_ok=True)
    h,interim=load_data();prices,price=price_data();beta,returns=estimate(prices)
    assumptions=build_assumptions(h,beta.iloc[0].beta);a=unpack(assumptions)
    ratios,kpi=analyze(h)
    year1=project(h,interim,a,1);year1_checks=run_model_checks(year1,interim,a,h);require_pass(year1_checks)
    # Sequential gate: Year 1 must pass before five years exist.
    model=project(h,interim,a);checks=run_model_checks(model,interim,a,h);require_pass(checks)
    v,discounts=dcf(model,interim,a,h);broken=broken_tests(model,interim,a,h)
    shocks,rates,cases,grid=sensitivities(h,interim,a,assumptions)
    implied=solve_implied(h,interim,a,price);abg=validate_abg()
    audit=independent_audit(h,interim,model,a,v,discounts,shocks,implied,prices)
    terminal=terminal_variants(v,model,a)
    wacc=pd.DataFrame([dict(valuation_date=ASOF,market_price=price,reported_basic_shares=46.7,market_equity=price*46.7,
        diluted_shares=50.7,diluted_market_equity=price*50.7,traditional_debt=0.,equity_weight=1.,debt_weight=0.,
        beta=beta.iloc[0].beta,risk_free_rate=.0475,erp=.0414,cost_of_equity=v['wacc'],pretax_cost_of_debt=0.,
        normalized_tax_rate=.24,aftertax_cost_of_debt=0.,wacc=v['wacc'],input_date='2026-09-01',
        debt_cost_note='Not applicable: no traditional debt; zero contribution, not a quoted borrowing rate')])
    yearly_ufcf=pd.DataFrame(index=model.index)
    for k in ['period_ebit','nopat','period_da','period_capex','delta_nwc','ufcf']:yearly_ufcf[k]=model[k]
    outputs={'historical_financials':h,'historical_ratios':ratios,'operating_kpis':kpi,'forecast_income_statement':model[IS].T,
       'forecast_balance_sheet':model[BS].T,'forecast_cash_flow':model[CF].T,'forecast_all_lines':model,
       'year1_forecast':year1.T,'year1_checks':year1_checks,'beta_statistics':beta,'monthly_returns':returns,
       'wacc':wacc,'dcf_discounting':discounts,'ufcf':yearly_ufcf,'sensitivity':shocks,'seven_discount_rates':rates,
       'named_cases':cases,'wacc_growth_grid':grid,'market_implied':implied,'broken_model_tests':broken,'independent_audit':audit,
       'abg_reference_validation':abg,'terminal_variants':terminal}
    for name,table in outputs.items():table.to_csv(tables/(name+'.csv'),index=True)
    assumptions.to_csv(ROOT/'assumptions.csv',index=False);checks.to_csv(ROOT/'model_checks.csv',index=False)
    (tables/'valuation.json').write_text(json.dumps(v,indent=2),encoding='utf8')
    figures=make_charts(h,model,v,shocks,rates,cases,grid,returns,beta.iloc[0],price,ROOT/'outputs/figures')
    result=dict(h=h,interim=interim,prices=prices,price=price,beta=beta,returns=returns,assumptions=assumptions,a=a,ratios=ratios,kpi=kpi,
      year1=year1,year1_checks=year1_checks,model=model,checks=checks,v=v,discounts=discounts,broken=broken,shocks=shocks,
      rates=rates,cases=cases,grid=grid,implied=implied,abg=abg,audit=audit,terminal=terminal,wacc=wacc,figures=figures)
    from .reporting import write_reports
    write_reports(result)
    return result
