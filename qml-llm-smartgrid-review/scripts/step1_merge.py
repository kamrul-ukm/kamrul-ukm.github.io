import pandas as pd, re, unicodedata, sys
s=pd.read_csv(sys.argv[1]); w=pd.read_excel(sys.argv[2])
S=pd.DataFrame({'db':'Scopus','authors':s['Authors'],'title':s['Title'],'year':s['Year'],'source':s['Source title'],
  'volume':s['Volume'],'issue':s['Issue'],'pages':s['Page start'].astype(str)+'-'+s['Page end'].astype(str),'artno':s['Art. No.'],
  'doi':s['DOI'],'abstract':s['Abstract'],'keywords':s['Index Keywords'],'doctype':s['Document Type'],'cited':s['Cited by'],'publisher':'' ,'id':s['EID']})
W=pd.DataFrame({'db':'WoS','authors':w['Authors'],'title':w['Article Title'],'year':w['Publication Year'],'source':w['Source Title'],
  'volume':w['Volume'],'issue':w['Issue'],'pages':w['Start Page'].astype(str)+'-'+w['End Page'].astype(str),'artno':w['Article Number'],
  'doi':w['DOI'],'abstract':w['Abstract'],'keywords':w['Author Keywords'].fillna('')+'; '+w['Keywords Plus'].fillna(''),
  'doctype':w['Document Type'],'cited':w['Times Cited, All Databases'],'publisher':w['Publisher'],'id':w['IDS Number']})
D=pd.concat([S,W],ignore_index=True)
def nt(t):
    t=unicodedata.normalize('NFKD',str(t)).lower(); t=re.sub(r'<[^>]+>','',t); return re.sub(r'[^a-z0-9]','',t)
D['doi_n']=D['doi'].fillna('').str.lower().str.strip().str.replace(r'^https?://(dx\.)?doi\.org/','',regex=True)
D['title_n']=D['title'].map(nt)
n0=len(D); counts={'scopus':len(S),'wos':len(W)}
# duplicates: DOI first, then normalised title (+ year +/-1 tolerance via title only)
D['dup']=False
seen_doi={}; seen_t={}
for i,r in D.iterrows():
    d=r['doi_n']; t=r['title_n']
    if d and d in seen_doi: D.at[i,'dup']=True; continue
    if t and t in seen_t: D.at[i,'dup']=True; continue
    if d: seen_doi[d]=i
    if t: seen_t[t]=i
dups=D[D.dup]; U=D[~D.dup].copy()
print('identified',counts,'total',n0,'duplicates',len(dups),'(within Scopus',(dups.db=='Scopus').sum(),', WoS',(dups.db=='WoS').sum(),') unique',len(U))
D.to_pickle('prisma/all.pkl'); U.to_pickle('prisma/unique.pkl')
