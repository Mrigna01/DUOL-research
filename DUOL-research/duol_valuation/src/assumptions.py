import pandas as pd
from .data_loader import LETTER,FILING

def build_assumptions(h, beta):
    b=h.loc[2025]; rows=[]
    def add(name,values,category,source,rationale,shock,low=None,high=None):
        if not isinstance(values,list):values=[values]*5
        for i,v in enumerate(values):
            cat=category[i] if isinstance(category,list) else category
            rows.append(dict(assumption_name=name,year=2026+i,base_value=v,source_category=cat,source=source,rationale=rationale,
                             downside_value=v-shock,upside_value=v+shock,guidance_low=low if i==0 else None,guidance_high=high if i==0 else None,
                             notes='Downside/upside columns are parameter low/high; value impact may reverse.'))
    add('growth',[1207/b.revenue-1,.18,.16,.13,.10],['GUIDANCE']+['JUDGMENT']*4,LETTER+' p10','2026 $1,207m point outlook; subsequent reacceleration then maturity is judgment.',.03,.15,.18)
    add('gross_margin',[.716,.72,.73,.74,.74],['GUIDANCE']+['JUDGMENT']*4,LETTER+' p10','2026 71.6% guidance; modest future recovery with AI delivery efficiency.',.01)
    add('rd_ex_sbc',[.23,.225,.22,.215,.21],'JUDGMENT',LETTER+' p21','R&D remains largest investment; includes allocated D&A, excludes equity compensation.',.01)
    add('sm_ex_sbc',[.13,.125,.12,.115,.11],'JUDGMENT',LETTER+' p21','Higher 2026 marketing effort, then gradual scale efficiency.',.01)
    add('ga_ex_sbc',[.105,.10,.095,.09,.085],'JUDGMENT',LETTER+' p21','Administrative operating leverage; includes D&A; no separate D&A charge in EBIT.',.01)
    add('sbc_ratio',[.15,.14,.13,.12,.11],['GUIDANCE']+['JUDGMENT']*4,LETTER+' p10','2026 equity expense guidance; gradually declining expense intensity thereafter.',.02)
    add('da_ratio',b.da/b.revenue,'HISTORY',FILING+' cash-flow statement p86','Carry FY2025 D&A/revenue; embedded in costs, added back once in cash flow.',.002)
    add('capex_ratio',b.capex/b.revenue,'HISTORY',FILING+' cash-flow statement p86','PPE plus software/intangible cash purchases; acquisitions excluded.',.005)
    add('tax_rate',.24,['GUIDANCE']+['JUDGMENT']*4,LETTER+' p10','Midpoint 23–25% effective tax outlook; normalized cash-tax proxy. No 2025 benefit recurrence.',.02,.23,.25)
    for name,key,shock in [('ar_ratio','ar',.02),('deferred_cost_ratio','deferred_cost',.01),('prepaid_ratio','prepaid',.005),('ap_ratio','ap',.003),('accrued_ratio','accrued',.01)]:
        add(name,b[key]/b.revenue,'HISTORY',FILING+' balance sheet p83','Carry FY2025 balance/revenue. Accrued includes current lease obligations on operating basis.',shock)
    add('deferred_revenue_ratio',(b.deferred_revenue+1285-1207)/1207,'JUDGMENT',LETTER+' p10; '+FILING+' p83','2026 bookings guidance minus revenue approximates deferred-revenue change; hold resulting ratio later. FX/other timing ignored.',.03)
    add('investment_yield',b.interest_income/(h.loc[2024,'cash']+h.loc[2024,'investments']),'HISTORY',FILING+' statements','Prior-year interest / opening cash and investments. Excluded from operating FCFF.',.01)
    add('minimum_cash',100.,'JUDGMENT','Analyst liquidity policy','Retain $100m operating cash; no assumed borrowing facility. Cash floor failure blocks valuation.',25.)
    add('buybacks',0.,'JUDGMENT',LETTER+' p9; Q2 10-Q cash flow p10','No incremental future discretionary repurchases in base; $71.9m through Aug1 vs $69.603m H1 cash is separately dated bridge adjustment.',10.)
    add('option_proceeds',0.,'JUDGMENT','Analyst financing policy','No speculative future option exercises; existing equity awards captured in diluted denominator.',5.)
    add('withholding_ratio',b.withholding/b.sbc,'HISTORY',FILING+' p85–86','Cash tax withholding on net-settled shares; reduces cash and equity, not EBIT or FCFF.',.05)
    add('ppe_capex_share',b.capex_ppe/b.capex,'HISTORY',FILING+' p86','Allocate capex between PPE and intangibles; allocate D&A by opening asset balances.',.05)
    add('diluted_shares',50.7,'HISTORY',LETTER+' p11','Latest estimated fully diluted shares; includes founder awards and RSUs. No extra future dilution multiplier with SBC expense retained.',1.)
    add('terminal_growth',.03,'JUDGMENT','Analyst long-run nominal USD assumption','Mature growth; recompute terminal working capital at 3%, hold margins and capex/D&A ratios.',.005)
    add('wacc',.0475+beta*.0414,'JUDGMENT','Damodaran Sept1 2026 Treasury 4.75%, ERP 4.14%; measured DUOL/SPY beta','Observed beta CAPM; traditional debt zero so WACC=cost of equity. Input vintage explicitly Sept1.',.01)
    return pd.DataFrame(rows)

def unpack(table):
    return {name:g.sort_values('year').base_value.to_numpy().copy() for name,g in table.groupby('assumption_name')}
