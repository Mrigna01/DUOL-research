"""Small reference reproduction of the equations disclosed in course slide notes."""
import pandas as pd
import numpy as np
from scipy.optimize import brentq

def reference(growth=.018,gm=.1705,capex=250.,sga_shift=0.,floor_rate=.0467,r=.1):
    revenue,ppe,inventory,fp,debt,cash,equity,other=17999.,3070.4,2135.8,2027.,3572.,40.4,3891.7,6371.6
    revolver=0.;flows=[]
    for i,sga in enumerate([.665,.655,.645,.645,.645]):
        rev=revenue*(1+growth);gp=rev*gm;da=ppe*82.4/3070.4
        ebit=gp-gp*(sga+sga_shift)-da-120
        pretax=ebit-fp*floor_rate-debt*.0544-revolver*.06;ni=pretax-max(pretax,0)*.255
        inv=(rev-gp)*2135.8/(17999-3071.7);newfp=inv*2027/2135.8;dw=(rev-revenue)*.008
        paydown=min(150,debt);fcfe=ni+da+120-capex-(inv-inventory)-dw+(newfp-fp)-paydown
        before=cash+fcfe-150;draw=min(max(25-before,0),max(850-revolver,0));repay=min(revolver,max(before-25,0))
        cash=before+draw-repay;revolver+=draw-repay;ppe+=capex-da;other+=dw-120;debt-=paydown;equity+=ni-150
        residual=cash+inv+ppe+other-newfp-debt-revolver-2127.5-equity
        assert abs(residual)<.05 and cash>=25-.05
        revenue,inventory,fp=rev,inv,newfp;flows.append(fcfe)
    return (sum(f/(1+r)**t for t,f in enumerate(flows,1))+(flows[-1]+150)*1.025/(r-.025)/(1+r)**5)/17.951349

def validate_abg():
    specs=[('Base',{},291.75),('GM down',{'gm':.1605},256.1),('GM up',{'gm':.1805},327.4),('Capex up',{'capex':300},258.3),('Capex down',{'capex':200},325.2),('Growth down',{'growth':.008},270.2),('Growth up',{'growth':.028},314.1),('Named downside',{'gm':.1605,'growth':.008,'sga_shift':.01,'floor_rate':.0567},210.0)]
    rows=[dict(test=n,calculated=reference(**kw),course_answer=e,tolerance=.005 if n=='Base' else .051) for n,kw,e in specs]
    for key,lo,hi,target in [('r',.08,.2,.1382),('gm',.1,.2,.1408),('capex',250,800,406.6)]:
        points=[]
        for x in np.linspace(lo,hi,301):
            try:points.append((x,reference(**{key:x})-183.29))
            except AssertionError:points.append((x,None))
        bracket=next((x,z) for (x,y),(z,w) in zip(points,points[1:]) if y is not None and w is not None and y*w<=0)
        root=brentq(lambda x:reference(**{key:x})-183.29,*bracket)
        rows.append(dict(test='Implied '+key,calculated=root,course_answer=target,tolerance=.001 if key!='capex' else .15))
    result=pd.DataFrame(rows);result['status']=result.apply(lambda x:'PASS' if abs(x.calculated-x.course_answer)<x.tolerance else 'FAIL',axis=1)
    if not result.status.eq('PASS').all():raise AssertionError(result.to_string())
    return result
