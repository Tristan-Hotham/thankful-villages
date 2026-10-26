"""Thankful Villages: luck or size? Wikipedia list of Thankful Villages matched to 2011 parish populations,
with a simple independent-risk model of the chance that every serving man returned."""
import json, re, numpy as np, pandas as pd
L=json.load(open('data/raw/thankful_villages.json'))
par=pd.read_csv('data/raw/parishes2011_ks101.csv'); par.columns=['code','name','pop']
par['nodata']=par.name.str.contains(r'\(no data\)'); par['name']=par.name.str.replace(r' \(no data\)','',regex=True)
pop=dict(zip(par.code,par['pop']))
norm=lambda s: re.sub(r'[^a-z]','',s.lower().split(',')[0].replace('st.','st').replace('saint','st'))
served={'Upper Slaughter':25,'Nether Kellet':21,'Stretton en le Field':11,'Harley, Shropshire':20,'Colwinston':23}
rows=[]
for x in L:
    p=x['parishes'][0] if x['parishes'] else [None,None,None]
    # same parish if the modern parish name starts with the village name
    v=norm(x['name'].split('/')[0].replace("''",'')); pn=norm(p[0] or '')
    same = pn.startswith(v) or v.startswith(pn)
    rows.append(dict(village=x['name'].split('/')[0], title=x['title'], county=x['county'], nation=x['nation'], doubly=x['doubly'],
        lat=x['lat'], lon=x['lon'], parish=p[0], parish_code=p[1], district=p[2], same_parish=same,
        pop2011=pop.get(p[1]) if same else np.nan, served=served.get(x['title'])))
T=pd.DataFrame(rows)
print(T[['village','parish','same_parish','pop2011','served']].to_string())
T.to_csv('results/thankful_villages.csv',index=False)

# fallback: match by name where the 2011 code is missing (codes changed after 2011 in reorganised areas)
byname=par.groupby(par.name.map(norm))
T.loc[T.village.str.startswith('South Elmham'),'same_parish']=True
for i,r in T.iterrows():
    if not r.same_parish or not np.isnan(r.pop2011): continue
    key=norm(r.parish)
    if key in byname.groups:
        g=par.loc[byname.groups[key]]
        if len(g)==1:
            T.loc[i,'pop2011']=g['pop'].iloc[0]; T.loc[i,'nodata2011']=bool(g.nodata.iloc[0])
T.loc[T.village.str.startswith('South Elmham'),'pop2011']=par.loc[par.name.str.contains('Michael, South Elmham|South Elmham St Michael',regex=True),'pop'].max()
print(T[T.same_parish][['village','parish','pop2011','nodata2011']].to_string())
nod={'Strethall','Knill','East Norton','Stretton en le Field','High Toynton','Culpho','Wordwell','South Elmham St Michael'}
T['nodata2011']=T.village.isin(nod)
S=T[T.same_parish].copy()
bands=[0,100,200,500,1000,1e9]; labs=['under 100','100–199','200–499','500–999','1,000+']
def band(p,nd): return 'under 100' if nd else labs[np.searchsorted(bands,p,side='right')-1]
S['band']=[band(p,n) for p,n in zip(S.pop2011,S.nodata2011)]
par['band']=[band(p,n or p!=p) for p,n in zip(par['pop'],par.nodata)]
cmp=pd.DataFrame({'parishes':par.band.value_counts(),'thankful':S.band.value_counts()}).reindex(labs).fillna(0)
cmp['rate_per_1000']=1000*cmp.thankful/cmp.parishes
cmp['share_parishes']=100*cmp.parishes/cmp.parishes.sum(); cmp['share_thankful']=100*cmp.thankful/cmp.thankful.sum()
print(cmp.round(2))
print('median TV pop2011 (with data):',S.pop2011.median(),' all parishes median:',par['pop'].median(), 'n parishes',len(par))
# luck model
d=0.12
for t,s in served.items():
    print(t,s,'P(all home)=%.3f'%((1-d)**s), 'served per 2011 resident', s/ T.set_index('title').pop2011.get(t,np.nan))
k=np.arange(0,61)
json.dump({'curve':[[int(n),round((1-d)**n,5)] for n in k]},open('results/curve.json','w'))
N=par['pop'].fillna(60).values
exp={}
for s in [0.06,0.09,0.13]:
    pr=(1-d)**(s*N); exp[s]=pr.sum()
    print('s=%.2f expected thankful parishes %.0f'%(s,pr.sum()), {b:round(pr[(par.band==b).values].sum()) for b in labs})
cmp['expected_s09']=[round(((1-d)**(0.09*N))[(par.band==b).values].sum(),1) for b in labs]
cmp.to_csv('results/size_bands.csv')
cmp['expected_s13']=[round(((1-d)**(0.13*N))[(par.band==b).values].sum(),1) for b in labs]
cmp['expected_s06']=[round(((1-d)**(0.06*N))[(par.band==b).values].sum(),1) for b in labs]
cmp.to_csv('results/size_bands.csv')
print(cmp.round(1))
import os; os.makedirs('data',exist_ok=True)
T['pop2011']=T.pop2011.where(~T.nodata2011)
out={'villages':json.loads(T.drop(columns=['title']).to_json(orient='records')),
     'bands':json.loads(cmp.reset_index().rename(columns={'index':'band'}).to_json(orient='records')),
     'expected':{str(k):round(v) for k,v in exp.items()}, 'd':d, 'n_parishes':int(len(par)),
     'served':[[t.split(',')[0],s,round((1-d)**s,3)] for t,s in served.items()]}
json.dump(out,open('data/thankful.json','w'),ensure_ascii=False)
