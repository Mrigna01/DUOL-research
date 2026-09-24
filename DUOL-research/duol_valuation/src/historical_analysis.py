import pandas as pd

def analyze(h):
    ratios=pd.DataFrame(index=h.index)
    ratios['revenue_growth']=h.revenue.pct_change()
    for k in ['gross_profit','ebit','rd','sm','ga','sbc','da','capex','deferred_revenue','ar','deferred_cost']:
        ratios[k+'_to_revenue']=h[k]/h.revenue
    ratios['effective_tax_rate']=h.tax/h.pretax
    ratios['cash_and_investments']=h.cash+h.investments
    ratios['basic_share_growth']=h.basic_shares.pct_change();ratios['diluted_share_growth']=h.diluted_shares.pct_change()
    kpi=pd.DataFrame({'year':[2023,2024,2025],'mau':[88.4,116.7,133.1],'dau':[26.9,40.5,52.7],'paid_subscribers':[6.6,9.5,12.2],
       'bookings':[622.181,870.601,1158.425],'subscription_bookings':[495.497,730.737,996.268],
       'subscription_revenue':[404.684,607.531,873.442]}).set_index('year')
    for key in ['mau','dau','paid_subscribers','bookings','subscription_revenue']:kpi[key+'_growth']=kpi[key].pct_change()
    kpi['paid_to_mau']=kpi.paid_subscribers/kpi.mau
    kpi['dau_to_mau']=kpi.dau/kpi.mau
    kpi['revenue_per_yearend_payer_proxy']=kpi.subscription_revenue/kpi.paid_subscribers
    return ratios,kpi
