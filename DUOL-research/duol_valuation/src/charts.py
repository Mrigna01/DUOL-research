import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import PercentFormatter,StrMethodFormatter

def make_charts(h,m,v,shocks,rates,cases,grid,returns,beta,price,out):
    out.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.titlesize':14,'figure.dpi':140})
    saved=[]
    def save(fig,name,note='Source: SEC filings and calculated DUOL model; USD. Educational analysis.'):
        fig.text(.02,.012,note,fontsize=8,color='#555555');fig.tight_layout(rect=(0,.045,1,1));fig.savefig(out/(name+'.png'),bbox_inches='tight');fig.savefig(out/(name+'.svg'),bbox_inches='tight');plt.close(fig);saved.append(name)
    fig,ax=plt.subplots(1,2,figsize=(12,4.6))
    ax[0].plot(h.index,h.revenue,'o-',color='#164b75',label='Actual');ax[0].plot([2025]+list(m.index),[h.loc[2025,'revenue']]+list(m.revenue),'o--',color='#008577',label='Forecast')
    ax[0].set(title='Revenue grows to $%.2fb in 2030'%(m.revenue.iloc[-1]/1000),ylabel='Revenue ($ millions)',xlabel='Fiscal year');ax[0].legend()
    ax[1].plot(h.index,h.ebit/h.revenue,'o-',label='Actual');ax[1].plot(m.index,m.operating_margin,'o--',label='Forecast');ax[1].yaxis.set_major_formatter(PercentFormatter(1));ax[1].set(title='Operating margin reaches %.1f%%'%(m.operating_margin.iloc[-1]*100),ylabel='EBIT / revenue',xlabel='Fiscal year');ax[1].legend();save(fig,'operating_performance')
    fig,ax=plt.subplots(figsize=(9,4.8));ax.plot(rates.wacc,rates.value_per_share,'o-',color='#008577');ax.axhline(price,color='#a44432',ls='--',label=f'Market close ${price:.2f}');ax.axvline(v['wacc'],color='#555',ls=':',label='Base WACC');ax.xaxis.set_major_formatter(PercentFormatter(1));ax.set(title='Seven discount rates change value materially',xlabel='WACC',ylabel='Value per diluted share ($)');ax.legend();save(fig,'seven_discount_rates')
    top=shocks.head(14).iloc[::-1];fig,ax=plt.subplots(figsize=(10,7));base=v['value_per_share']
    labels={'wacc':'WACC (±1 pp)','growth':'Revenue growth (±3 pp)','sbc_ratio':'SBC / revenue (±2 pp)','terminal_growth':'Terminal growth (±0.5 pp)','rd_ex_sbc':'R&D ex-SBC (±1 pp)','sm_ex_sbc':'Marketing ex-SBC (±1 pp)','ga_ex_sbc':'G&A ex-SBC (±1 pp)','gross_margin':'Gross margin (±1 pp)','capex_ratio':'Capex / revenue (±0.5 pp)','tax_rate':'Tax rate (±2 pp)','diluted_shares':'Diluted shares (±1m)','deferred_revenue_ratio':'Deferred revenue ratio (±3 pp)','da_ratio':'D&A / revenue (±0.2 pp)','ar_ratio':'Receivables ratio (±2 pp)'}
    ax.barh(top.assumption.map(labels),top.upside-top.downside,left=top.downside,color='#52afa2');ax.axvline(base,color='#164b75',ls='--',label=f'Base ${base:.2f}');ax.axvline(price,color='#ad4933',ls=':',label=f'Market ${price:.2f}')
    ax.set(title=f'WACC produces the largest tested swing: ${shocks.iloc[0].absolute_sensitivity:.0f}/share',xlabel='Value per diluted share ($)');ax.legend();save(fig,'assumption_tornado','Source: complete checked model reruns. Top 14 drivers; all scenarios in sensitivity.csv. pp = percentage points.')
    fig,ax=plt.subplots(figsize=(11,3.4));items=[('Market',price)]+[(r.case,r.value_per_share) for r in cases.iloc[:3].itertuples()]
    for j,(name,x) in enumerate(sorted(items,key=lambda x:x[1])):
        ax.scatter(x,0,s=100);ax.annotate(f'{name}\n${x:.2f}',(x,0),xytext=(0,35 if j%2==0 else -48),textcoords='offset points',ha='center')
    ax.axhline(0,color='#aaa',zorder=0);ax.set(ylim=(-1,1),yticks=[],xlabel='Value or price per diluted share ($)',title='Market price alongside complete operating cases');ax.spines['left'].set_visible(False);save(fig,'price_case_comparison')
    mat=grid.pivot(index='terminal_growth',columns='wacc',values='value_per_share');fig,ax=plt.subplots(figsize=(10,5));im=ax.imshow(mat,aspect='auto',cmap='Blues');ax.set_xticks(range(len(mat.columns)),[f'{x:.2%}' for x in mat.columns]);ax.set_yticks(range(len(mat)),[f'{x:.1%}' for x in mat.index]);ax.set(xlabel='WACC',ylabel='Terminal growth',title='Terminal assumptions produce a range of values ($/share)')
    for (i,j),val in np.ndenumerate(mat.values):ax.text(j,i,f'{val:.0f}',ha='center',va='center',color='white' if (val-mat.values.min())/(mat.values.max()-mat.values.min())>.5 else '#111',fontweight='bold' if i==2 and j==3 else 'normal')
    fig.colorbar(im,ax=ax,label='Value per share ($)');save(fig,'wacc_growth_heatmap')
    fig,ax=plt.subplots(figsize=(8,5));x=returns.SPY;y=returns.DUOL;ax.scatter(x,y,alpha=.7,color='#008577');line=np.linspace(x.min(),x.max(),100);ax.plot(line,beta.alpha_monthly+beta.beta*line,color='#a44432');ax.xaxis.set_major_formatter(PercentFormatter(1));ax.yaxis.set_major_formatter(PercentFormatter(1));ax.set(xlabel='SPY monthly price return',ylabel='DUOL monthly price return',title=f'60 monthly returns: beta {beta.beta:.3f}, R² {beta.r_squared:.3f}');save(fig,'beta_regression','Source: Yahoo monthly closes Aug2021–Aug2026; OLS with intercept. Adjusted-price robustness in beta_statistics.csv.')
    fig,ax=plt.subplots(figsize=(9,4.8));ax.bar(m.index,m.ufcf,color='#008577');ax.set(title='Operating cash flow after charging stock compensation',xlabel='Forecast period (2026 = H2 only)',ylabel='UFCF ($ millions)');save(fig,'ufcf_forecast')
    return saved
