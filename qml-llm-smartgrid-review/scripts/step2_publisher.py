import pandas as pd, re
U=pd.read_pickle('prisma/unique.pkl')
P={'10.1109':'IEEE','10.23919':'IEEE','10.1016':'Elsevier','10.3390':'MDPI','10.1007':'Springer','10.1038':'Springer Nature','10.1186':'Springer (BMC)',
   '10.1140':'Springer','10.1145':'ACM','10.1002':'Wiley','10.1049':'Wiley (IET)','10.1111':'Wiley','10.1155':'Wiley (Hindawi)'}
def pub(r):
    d=str(r['doi_n']); m=re.match(r'(10\.\d+)',d)
    if m and m.group(1) in P: return P[m.group(1)]
    if m: return 'OTHER:'+m.group(1)
    p=str(r['publisher']).upper(); src=str(r['source']).lower()
    for k,v in [('IEEE','IEEE'),('ELSEVIER','Elsevier'),('SPRINGER','Springer'),('COMPUTING MACHINERY','ACM'),('WILEY','Wiley'),('MDPI','MDPI')]:
        if k in p: return v
    for k,v in [('ieee','IEEE'),('lecture notes','Springer'),('communications in computer and information science','Springer'),('acm','ACM'),('procedia','Elsevier'),('ifac','Elsevier'),('iet ','Wiley (IET)'),('cired','Wiley (IET)')]:
        if k in src: return v
    return 'UNVERIFIED'
U['pub']=U.apply(pub,axis=1)
U['pub_ok']=~U['pub'].str.startswith(('OTHER','UNVERIFIED'))
print(U['pub'].value_counts().head(30).to_dict())
print('in-scope publishers',U.pub_ok.sum(),'removed',(~U.pub_ok).sum())
print(U.loc[U.pub=='UNVERIFIED',['source']].value_counts().head(20))
U.to_pickle('prisma/unique_pub.pkl')
