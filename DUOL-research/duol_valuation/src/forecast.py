"""Cash is computed last. FY2026 combines actual H1 and a separately linked H2."""
import pandas as pd

ASSET_KEYS=['cash','short_investments','long_investments','ar','deferred_cost','prepaid','tax_receivable','ppe','intangibles','rou','goodwill','restricted_cash','dta','other_assets']
LIABILITY_KEYS=['ap','accrued','deferred_revenue','tax_payable','lease_noncurrent','dtl','other_liabilities']
FLOWS=['revenue','cost_of_revenue','gross_profit','rd','sm','ga','opex','ebit','interest_income','other_net','pretax','tax','net_income','sbc','da','capex','capex_ppe','capex_software','cfo','cfi','cff']

def project_year(prev, prior_revenue, a, i, h1=None):
    y={k:prev[k] for k in ASSET_KEYS+LIABILITY_KEYS+['assets','liabilities','equity','nwc']};y['year']=2026+i
    v=lambda k:float(a[k][i])
    revenue=prior_revenue*(1+v('growth'))
    target={'revenue':revenue,'gross_profit':revenue*v('gross_margin'),'sbc':revenue*v('sbc_ratio'),
            'da':revenue*v('da_ratio'),'capex':revenue*v('capex_ratio')}
    # SBC allocation is presentation-only; total SBC independently drives operating profit.
    for key,weight in [('rd',.7),('sm',.1),('ga',.2)]:target[key]=revenue*v(key+'_ex_sbc')+weight*target['sbc']
    for k,val in target.items():y['period_'+k]=val-(h1[k] if h1 else 0)
    y['period_cost_of_revenue']=y['period_revenue']-y['period_gross_profit']
    y['period_opex']=sum(y['period_'+k] for k in ['rd','sm','ga'])
    y['period_ebit']=y['period_gross_profit']-y['period_opex']
    fraction=184/365 if h1 else 1.
    y['period_interest_income']=(prev['cash']+prev['short_investments']+prev['long_investments'])*v('investment_yield')*fraction
    y['period_other_net']=0.
    y['period_pretax']=y['period_ebit']+y['period_interest_income']
    y['period_tax']=max(0.,y['period_pretax'])*v('tax_rate')
    y['period_net_income']=y['period_pretax']-y['period_tax']
    for k in ['ar','deferred_cost','prepaid','ap','accrued','deferred_revenue']:y[k]=revenue*v(k+'_ratio')
    y['nwc']=sum(y[k] for k in ['ar','deferred_cost','prepaid'])-sum(y[k] for k in ['ap','accrued','deferred_revenue'])
    y['delta_nwc']=y['nwc']-prev['nwc']
    y['period_capex_ppe']=y['period_capex']*v('ppe_capex_share')
    y['period_capex_software']=y['period_capex']-y['period_capex_ppe']
    y['period_da_ppe']=y['period_da']*prev['ppe']/(prev['ppe']+prev['intangibles'])
    y['period_da_intangibles']=y['period_da']-y['period_da_ppe']
    y['ppe']=prev['ppe']+y['period_capex_ppe']-y['period_da_ppe']
    y['intangibles']=prev['intangibles']+y['period_capex_software']-y['period_da_intangibles']
    y['period_cfo']=y['period_net_income']+y['period_da']+y['period_sbc']-y['delta_nwc']
    y['period_cfi']=-y['period_capex'] # investment portfolio constant; roll maturities into same balances
    y['period_withholding']=y['period_sbc']*v('withholding_ratio')
    y['period_buybacks']=max(0.,v('buybacks'))*fraction
    if i==0:y['period_buybacks']+=71.9-69.603
    y['period_option_proceeds']=max(0.,v('option_proceeds'))*fraction
    y['period_cff']=y['period_option_proceeds']-y['period_withholding']-y['period_buybacks']
    y['equity']=prev['equity']+y['period_net_income']+y['period_sbc']+y['period_cff']
    y['cash']=prev['cash']+y['period_cfo']+y['period_cfi']+y['period_cff']
    y['assets']=sum(y[k] for k in ASSET_KEYS)
    y['liabilities']=sum(y[k] for k in LIABILITY_KEYS)
    y['nopat']=y['period_ebit']-max(0.,y['period_ebit'])*v('tax_rate')
    y['ufcf']=y['nopat']+y['period_da']-y['period_capex']-y['delta_nwc']
    # No SBC add-back in UFCF: economic compensation remains an expense.
    for k in FLOWS:y[k]=y['period_'+k]+(h1[k] if h1 else 0.)
    y['operating_margin']=y['ebit']/y['revenue']; y['minimum_cash']=v('minimum_cash')
    y['debt']=0.;y['financing_draw']=0.
    return y

def project(history,interim,a,n=5):
    prev=dict(interim);prior_revenue=float(history.loc[2025,'revenue']);rows=[]
    for i in range(n):
        y=project_year(prev,prior_revenue,a,i,interim if i==0 else None)
        h1_ufcf=(interim['ebit']-max(0.,interim['ebit'])*a['tax_rate'][0]+interim['da']-interim['capex']-(interim['nwc']-history.loc[2025,'nwc'])) if i==0 else 0.
        y['annual_ufcf']=y['ufcf']+h1_ufcf
        rows.append(y);prev=y;prior_revenue=y['revenue']
    return pd.DataFrame(rows).set_index('year')
