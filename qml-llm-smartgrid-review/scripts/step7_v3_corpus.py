import pandas as pd, json, re
U=pd.read_pickle('prisma/v3_unique.pkl'); E=pd.read_pickle('prisma/eligible.pkl')
inc_idx=U.index[U.v3_decision=='INCLUDED']
P=E.loc[inc_idx].copy()
P['cited']=pd.to_numeric(P.cited,errors='coerce').fillna(0)
qsub=['VQC/QNN','Quantum kernel/QSVM','QLSTM/quantum RNN','Annealing/QAOA/QUBO','Quantum linear/simulation','Quantum RL/FL']
P['Qcore']=P[['t_'+k for k in qsub]].any(axis=1)|(P.fam_Q&~P.fam_P)
P=P.sort_values(['year','title']).reset_index(); P['rid']=range(len(P))
R=E[E.is_review].copy(); R['cited']=pd.to_numeric(R.cited,errors='coerce').fillna(0); R=R.reset_index(); R['rv']=range(len(R))
P.to_pickle('prisma/v3_primary.pkl'); R.to_pickle('prisma/v3_reviews.pkl')
# map old keys
oP=pd.read_pickle('prisma/primary.pkl'); oR=pd.read_pickle('prisma/reviews.pkl')
def key(df): return {(r.doi_n if r.doi_n else r.title_n):r for r in df.itertuples()}
nP={ (r.doi_n if r.doi_n else r.title_n):r.rid for r in P.itertuples()}; nPt={r.title_n:r.rid for r in P.itertuples()}
nR={ (r.doi_n if r.doi_n else r.title_n):r.rv for r in R.itertuples()}; nRt={r.title_n:r.rv for r in R.itertuples()}
U2={ (r.doi_n if r.doi_n else r.title_n):(r.v3_decision,r.v3_reason) for r in U.itertuples()}
m={}
for r in oP.itertuples():
    k=r.doi_n if r.doi_n else r.title_n
    if k in nP or r.title_n in nPt: m[f'c{r.rid}']=f'c{nP.get(k,nPt.get(r.title_n))}'
    else: m[f'c{r.rid}']=('EXCL',U2.get(k,('?','?')))
for r in oR.itertuples():
    k=r.doi_n if r.doi_n else r.title_n
    m[f'r{r.rv}']=f'r{nR.get(k,nRt.get(r.title_n))}' if (k in nR or r.title_n in nRt) else ('EXCL',U2.get(k))
json.dump({k:(v if isinstance(v,str) else 'EXCL') for k,v in m.items()},open('prisma/keymap.json','w'))
cited=set(re.findall(r'\b([cr]\d+)\b',open('content2.js').read()))
for k in sorted(cited):
    if k in m and not isinstance(m[k],str): print(k,m[k], oP.loc[oP.rid==int(k[1:]),'title'].values[:1] if k[0]=='c' else '')
# stats
S={}
S['primary']=len(P); S['reviews']=len(R)
S['Q']=int(P.Qcore.sum()); S['L']=int(P.fam_L.sum()); S['P']=int(P.fam_P.sum()); S['QL']=int((P.Qcore&P.fam_L).sum())
segs=[c for c in P.columns if c.startswith('seg_')]
S['seg']={s[4:]:int(P[s].sum()) for s in segs}
S['segfam']={s[4:]:[int((P[s]&P.Qcore).sum()),int((P[s]&P.fam_L).sum()),int((P[s]&P.fam_P).sum())] for s in segs}
S['tech']={c[2:]:int(P[c].sum()) for c in P.columns if c.startswith('t_')}
S['year']={int(k):int(v) for k,v in P.year.value_counts().sort_index().items()}
S['yearfam']={int(y):[int(((P.year==y)&P.Qcore).sum()),int(((P.year==y)&P.fam_L).sum()),int(((P.year==y)&P.fam_P).sum())] for y in range(2018,2027)}
pub=P.pub.replace({'Springer Nature':'Springer','Springer (BMC)':'Springer','Wiley (IET)':'Wiley','Wiley (Hindawi)':'Wiley'}).value_counts()
S['pub']={k:int(v) for k,v in pub.items()}
dt=P.doctype.astype(str); S['conf']=int(dt.str.contains('Conference|Proceedings').sum()); S['art']=len(P)-S['conf']
b=P[P.ta.str.contains(r'billing|\bbills?\b|tariff|customer service|customer (?:query|queries|complaint|support)|call center|electricity (?:sales|marketing)|power marketing|contract|settlement')]
S['billing_specific']=len(b)
S['QLlist']=[(int(r.rid),r.title) for r in P[P.Qcore&P.fam_L].itertuples()]
json.dump(S,open('prisma/v3_stats.json','w'),indent=1); print(json.dumps({k:v for k,v in S.items() if k!='QLlist'},indent=0)); print(S['QLlist'])
