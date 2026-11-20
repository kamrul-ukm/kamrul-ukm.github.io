import pandas as pd, re, json
A=pd.read_pickle('prisma/all.pkl'); U=pd.read_pickle('prisma/unique_pub.pkl')
X=pd.read_pickle('prisma/screen1.pkl'); I=pd.read_pickle('prisma/screened_included.pkl'); E=pd.read_pickle('prisma/eligible.pkl')
def low(*c): return ' '.join(str(x) for x in c if isinstance(x,str)).lower()
U['ta']=U.apply(lambda r: low(r['title'],r['abstract']),axis=1)
dec=pd.Series('',index=U.index); sub=pd.Series('',index=U.index)
# --- Incomplete records (screening stage)
ab=U['abstract'].fillna('').astype(str)
inc_mask=(U['title'].isna())|(U['authors'].isna())|(U['year'].isna())|(ab.str.len()<300)|(ab.str.contains(r'\[no abstract available\]',case=False))|(U['doctype'].astype(str).str.contains('Retract'))|(U['title'].astype(str).str.contains(r'^retracted|retraction',case=False))|((U['doi_n']=='')&(U['source'].isna()))
# --- Not in scope
yr=pd.to_numeric(U['year'],errors='coerce')
for i in U.index:
    if not U.at[i,'pub_ok']: dec[i]='Not in scope'; sub[i]='Publisher outside IEEE/Elsevier/Springer/ACM/Wiley/MDPI ('+U.at[i,'pub']+')'; continue
    if yr[i]>2026 or yr[i]<2018: dec[i]='Not in scope'; sub[i]='Publication year outside 2018–2026'; continue
    if inc_mask[i]: dec[i]='Incomplete'; sub[i]='Missing abstract / authors / year / source, or retracted record'; continue
    d=X.at[i,'decision'] if i in X.index else 'INCLUDE'
    if d!='INCLUDE':
        if d.startswith('EC7'): dec[i]='Incomplete'; sub[i]='Missing or insufficient abstract'
        else: dec[i]='Not in scope'; sub[i]=d.split(': ',1)[1]
        continue
    e=I.at[i,'elig']
    if e!='ELIGIBLE': dec[i]='Not in scope'; sub[i]=e.split(': ',1)[1]; continue
    dec[i]='ELIGIBILITY'
# --- No experiment or no grid data (eligibility stage)
EXP=re.compile(r'experiment|results|we show|shows? that|shown that|found that|findings|tested|trial|simulat|case stud|test(?:ed|ing)? (?:on|in|with|using)|validat|evaluat|results (?:show|demonstrate|indicate|reveal)|numerical (?:result|stud|analys)|benchmark|compar(?:ed|ison|ative)|outperform|achiev|improv\w* (?:by|of)|reduc\w* (?:by|of)|accuracy|rmse|mape|\bmae\b|f1|precision|recall|\d+(?:\.\d+)?\s?%|implement(?:ed|ation)|prototype|testbed|test bed|hardware[- ]in[- ]the[- ]loop|\bhil\b|field (?:test|trial|demonstration)|demonstrat|performance (?:analysis|evaluation)|execution time|latency|throughput|computation(?:al)? (?:cost|overhead|time)|security analysis|proverif|avispa|scyther|random oracle|formal (?:security|verification)')
DATA=re.compile(r'\bdata\b|test (?:case|system|feeder|network|grid|instance)|instances?\b|\bbus\b|\bnodes?\b|ieee rts|rts-\d+|scenario|benchmark|real|measured|historical|case stud|ieee[- ]?\d+[- ]?(?:bus|node)|\d+[- ](?:bus|node)\b|bus system|test system|test feeder|feeder|real[- ]world|real (?:data|grid|utility|operational|measurement)|utility data|operational data|historical data|measured data|field data|dataset|data set|data from|data of|collected|smart meter data|meter data|load data|consumption data|ami data|scada data|pmu data|synchrophasor data|matpower|opendss|pandapower|gridlab|psse|pscad|digsilent|rtds|opal|ercot|caiso|pjm|miso|\bnem\b|entso|elia|state grid|sgcc|kaggle|ampds|uk-dale|ukdale|redd|pecan|nrel|gefcom|irish|cer\b|london|microgrid (?:testbed|laboratory|lab)|testbed|test bed|hardware[- ]in[- ]the[- ]loop|\bhil\b|power grid (?:company|corporation)|province|substation|distribution network of|wind farm|pv plant|solar farm|building|household|smart grid (?:scenario|environment|communication|network)|ami|advanced metering|scada|iec 61850|ieee 2030\.5|dlms|v2g|electric vehicle|charging')
GD=re.compile(r'grid|power|power system|distribution system|transmission|feeder|microgrid|smart meter|meter|load|wind|solar|irradiance|photovoltaic|\\bpv\\b|price|market|charging|electric|energy|substation|scada|pmu|unit commitment|dispatch|generator|voltage|frequency|utility|consumption|building|household|battery|storage')
ELI=U[dec=='ELIGIBILITY']
review=ELI.index.isin(E.index[E.is_review])
for k,i in enumerate(ELI.index):
    ta=U.at[i,'ta']
    if review[k]: dec[i]='No experiment or no grid data'; sub[i]='Review / survey / perspective (no original experiment; used as background)'; continue
    ex=bool(EXP.search(ta)); da=bool(DATA.search(ta))
    if ex and not da:
        sents=re.split(r'(?<=[.;!?]) ',ta)
        da=any(EXP.search(x) and GD.search(x) for x in sents) or bool(GD.search(str(U.at[i,'title']).lower()))
    if not ex and not da: dec[i]='No experiment or no grid data'; sub[i]='Neither experimental evaluation nor grid data / test system reported'
    elif not ex: dec[i]='No experiment or no grid data'; sub[i]='No experimental evaluation reported (conceptual / framework only)'
    elif not da: dec[i]='No experiment or no grid data'; sub[i]='No grid data, test system or grid scenario reported'
    else: dec[i]='INCLUDED'
U['v3_decision']=dec; U['v3_reason']=sub
U.to_pickle('prisma/v3_unique.pkl')
c={'scopus':int((A.db=='Scopus').sum()),'wos':int((A.db=='WoS').sum()),'total':len(A),'dup':int(A.dup.sum()),'dup_scopus':int((A.dup&(A.db=='Scopus')).sum()),'dup_wos':int((A.dup&(A.db=='WoS')).sum()),'unique':len(U)}
c['screened']=len(U)
nis=U[U.v3_decision=='Not in scope']; c['not_in_scope']=len(nis); r=nis.v3_reason.where(~nis.v3_reason.str.startswith('Publisher outside'),'Publisher outside IEEE/Elsevier/Springer/ACM/Wiley/MDPI'); c['not_in_scope_sub']={k:int(v) for k,v in r.value_counts().items()}
incm=U[U.v3_decision=='Incomplete']; c['incomplete']=len(incm)
c['assessed']=int(U.v3_decision.isin(['No experiment or no grid data','INCLUDED']).sum())
ne=U[U.v3_decision=='No experiment or no grid data']; c['noexp']=len(ne); c['noexp_sub']={k:int(v) for k,v in ne.v3_reason.value_counts().items()}
c['included']=int((U.v3_decision=='INCLUDED').sum())
json.dump(c,open('prisma/v3_counts.json','w'),indent=1,ensure_ascii=False); print(json.dumps(c,indent=1,ensure_ascii=False))
