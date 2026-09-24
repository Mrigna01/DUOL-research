"""Load frozen public sources; never substitute missing facts silently."""
from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data/raw'
PROCESSED = ROOT / 'data/processed'
ASOF = '2026-09-21'
FILING = 'https://www.sec.gov/Archives/edgar/data/1562088/000162828026012494/duol-20251231.htm'
LETTER = 'https://www.sec.gov/Archives/edgar/data/1562088/000162828026053299/q2fy26duolingo6-30x26share.htm'
FACTS = json.loads((RAW/'companyfacts.json').read_text())['facts']['us-gaap']
LEDGER = []

TAGS = {
 'revenue':'RevenueFromContractWithCustomerExcludingAssessedTax',
 'cost_of_revenue':'CostOfRevenue','gross_profit':'GrossProfit',
 'rd':'ResearchAndDevelopmentExpense','sm':'SellingAndMarketingExpense',
 'ga':'GeneralAndAdministrativeExpense','opex':'OperatingExpenses',
 'ebit':'OperatingIncomeLoss','interest_income':'InterestIncomeOperating',
 'other_net':'NonoperatingIncomeExpense','pretax':'IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest',
 'tax':'IncomeTaxExpenseBenefit','net_income':'NetIncomeLoss',
 'da':'DepreciationDepletionAndAmortization','sbc':'ShareBasedCompensation',
 'capex_ppe':'PaymentsToAcquirePropertyPlantAndEquipment','capex_software':'PaymentsForSoftware',
 'cfo':'NetCashProvidedByUsedInOperatingActivities','cfi':'NetCashProvidedByUsedInInvestingActivities',
 'cff':'NetCashProvidedByUsedInFinancingActivities','options_proceeds':'ProceedsFromStockOptionsExercised',
 'withholding':'PaymentsRelatedToTaxWithholdingForShareBasedCompensation',
 'investment_purchases':'PaymentsToAcquireInvestments','investment_maturities':'ProceedsFromSaleMaturityAndCollectionsOfInvestments',
 'cf_deferred_revenue_increase':'IncreaseDecreaseInContractWithCustomerLiability',
 'cf_ar_increase':'IncreaseDecreaseInAccountsReceivable','cf_ap_increase':'IncreaseDecreaseInAccountsPayable',
 'cf_accrued_increase':'IncreaseDecreaseInAccruedLiabilities',
 'diluted_shares':'WeightedAverageNumberOfDilutedSharesOutstanding',
 'cash':'CashAndCashEquivalentsAtCarryingValue','short_investments':'DebtSecuritiesHeldToMaturityAmortizedCostAfterAllowanceForCreditLossCurrent',
 'long_investments':'LongTermInvestments','ar':'AccountsReceivableNetCurrent',
 'deferred_cost':'CapitalizedContractCostNetCurrent','prepaid':'PrepaidExpenseAndOtherAssetsCurrent',
 'tax_receivable':'IncomeTaxReceivable','ppe':'PropertyPlantAndEquipmentNet',
 'intangibles':'IntangibleAssetsNetExcludingGoodwill','rou':'OperatingLeaseRightOfUseAsset',
 'goodwill':'Goodwill','restricted_cash':'RestrictedCashNoncurrent','dta':'DeferredIncomeTaxAssetsNet',
 'other_assets':'OtherAssetsNoncurrent','assets':'Assets','ap':'AccountsPayableCurrent',
 'accrued':'AccruedLiabilitiesCurrent','deferred_revenue':'ContractWithCustomerLiabilityCurrent',
 'tax_payable':'AccruedIncomeTaxesCurrent','lease_noncurrent':'OperatingLeaseLiabilityNoncurrent',
 'dtl':'DeferredIncomeTaxLiabilitiesNet',
 'liabilities':'Liabilities','equity':'StockholdersEquity'}
BS = list(TAGS)[list(TAGS).index('cash'):]

def fact(tag, end, start=None, optional_zero=False):
    candidates = [v for values in FACTS.get(tag,{}).get('units',{}).values() for v in values
                  if v['end']==end and v.get('start')==start and v['filed']<=ASOF
                  and v['form'] in ['10-K','10-Q']]
    if not candidates:
        if optional_zero:
            LEDGER.append(dict(metric=tag,end=end,start=start,value=0,source='Absent line confirmed from filing; no balance/activity'))
            return 0.
        raise ValueError(f'Missing source: {tag}, {start}, {end}')
    v=sorted(candidates,key=lambda x:(x['form']=='10-K',x['filed']))[-1]
    LEDGER.append(dict(metric=tag,end=end,start=start,value=v['val']/1e6,source=f"SEC {v['accn']} ({v['filed']}); companyfacts",tag=tag))
    return v['val']/1e6

def load_data():
    LEDGER.clear()
    rows=[]
    for year,end,start in [(2023,'2023-12-31','2023-01-01'),(2024,'2024-12-31','2024-01-01'),(2025,'2025-12-31','2025-01-01'),(2026,'2026-06-30','2026-01-01')]:
        row={'year':year}
        for key,tag in TAGS.items():
            optional=(year==2023 and key in ['short_investments','long_investments','investment_purchases','investment_maturities','goodwill','tax_receivable','dtl'])
            if key=='capex_software' and year<2026:
                row[key]={2023:10.493,2024:9.024,2025:9.303}[year]
                LEDGER.append(dict(metric=key,end=end,start=start,value=row[key],source=FILING+'; cash-flow statement p86; software AND acquired intangibles'))
            else:
                row[key]=fact(tag,end,None if key in BS else start,optional)
        row['basic_shares']={2023:41.451,2024:43.504,2025:45.773,2026:46.744}[year]
        row['share_repurchases']={2023:0.,2024:0.,2025:0.,2026:69.603}[year]
        row['cf_deferred_cost_increase']={2023:18.890,2024:26.231,2025:22.501,2026:.026}[year]
        if year<2026:
            row['other_income']={2023:.590,2024:1.267,2025:3.382}[year]
            row['other_expense']={2023:.645,2024:4.253,2025:1.773}[year]
        row['capex']=row['capex_ppe']+row['capex_software']
        row['other_net']=row['pretax']-row['ebit']-row['interest_income']
        row['investments']=row['short_investments']+row['long_investments']
        row['other_liabilities']=row['liabilities']-row['ap']-row['accrued']-row['deferred_revenue']-row['tax_payable']-row['lease_noncurrent']-row['dtl']
        row['nwc']=row['ar']+row['deferred_cost']+row['prepaid']-row['ap']-row['accrued']-row['deferred_revenue']
        rows.append(row)
    history=pd.DataFrame(rows[:3]).set_index('year'); interim=rows[3]
    PROCESSED.mkdir(exist_ok=True,parents=True)
    history.to_csv(PROCESSED/'historical_financials.csv')
    pd.Series(interim).to_csv(PROCESSED/'h1_2026.csv')
    pd.DataFrame(LEDGER).to_csv(PROCESSED/'source_ledger.csv',index=False)
    return history,interim

def price_data():
    frames=[]
    for symbol in ['DUOL','SPY']:
        x=json.loads((RAW/f'{symbol}-prices.json').read_text())['chart']['result'][0]
        dates=pd.to_datetime(x['timestamp'],unit='s',utc=True).tz_convert('America/New_York').tz_localize(None).to_period('M')
        frame=pd.DataFrame({symbol:x['indicators']['quote'][0]['close'],symbol+'_adjusted':x['indicators']['adjclose'][0]['adjclose']},index=dates)
        frames.append(frame[~frame.index.duplicated(keep='last')])
    prices=pd.concat(frames,axis=1).loc['2021-08':'2026-08']
    if len(prices)!=61 or prices.isna().any().any():raise ValueError('Incomplete beta price window')
    prices.to_csv(PROCESSED/'monthly_prices.csv')
    x=json.loads((RAW/'DUOL-daily.json').read_text())['chart']['result'][0]
    daily=pd.Series(x['indicators']['quote'][0]['close'],index=pd.to_datetime(x['timestamp'],unit='s',utc=True).strftime('%Y-%m-%d'))
    price=round(float(daily.loc[ASOF]),2)
    return prices,price
