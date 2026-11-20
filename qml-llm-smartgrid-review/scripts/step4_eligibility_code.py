import pandas as pd, re
X=pd.read_pickle('prisma/screen1.pkl'); inc=X[X.decision=='INCLUDE'].copy()
T=re.compile(r'qubit|quantum|qaoa|qubo|annealer|large language|\bllms?\b|\bgpt|chatgpt|foundation model|retrieval[- ]augmented|\brag\b|language model|deepseek|qwen|llama|vision[- ]language|multimodal large|agentic|\bagent|generative|post[- ]quantum|lattice|\bqkd\b|kyber|dilithium|sphincs|large model|pre-?trained model|big model|\bslm')
LOAD=re.compile(r'data cent(?:er|re)|gpu power|ai workload|computing load|ai load|power hungry|ai computing')
def elig(r):
    tl=str(r['title']).lower()
    if LOAD.search(tl) and not re.search(r'llm[- ]based|using (?:a )?(?:large )?language|llm-driven|llm agent',tl): return 'EX-E3: AI/LLM as electrical load, not as method'
    if not T.search(r['tk']): return 'EX-E1: technique not central (absent from title & keywords)'
    return 'ELIGIBLE'
inc['elig']=inc.apply(elig,axis=1)
print(inc.elig.value_counts().to_dict())
E=inc[inc.elig=='ELIGIBLE'].copy()
E['is_review']=E.doctype.str.contains('Review')|E.title.str.lower().str.contains(r'\breview\b|survey|state of the art|state-of-the-art|overview|perspective|roadmap|tutorial|primer|systematic literature|bibliometric')
ta=E.ta
def has(p): return ta.str.contains(p,regex=True)
seg={
 'Generation': has(r'unit commitment|economic dispatch|generation (?:schedul|expansion|planning)|power plant|wind (?:power|farm|turbine|speed)|solar (?:power|irradiance|radiation)|photovoltaic power|pv power|renewable (?:energy )?(?:forecast|generation|scenario)|capacity expansion|hydropower|nuclear power|thermal power|generator'),
 'Transmission': has(r'transmission (?:line|system|network|grid|tower)|transient stability|voltage stability|small-signal|power flow|state estimation|substation|\bpmu|synchrophasor|iec 61850|protection relay|line protection|power transformer|transformer fault|insulator|power inspection|bulk power|contingency|electromagnetic transient|\bemt\b|security[- ]constrained|optimal power flow|\bscada\b|dispatch(?:ing)? (?:center|centre|operation|instruction|order)|power grid dispatch|grid dispatch'),
 'Distribution & DER': has(r'distribution (?:network|system|grid|feeder|transformer)|microgrid|micro-grid|distributed energy|\bders?\b|distributed (?:photovoltaic|pv|generation)|energy storage|battery|voltage (?:control|regulation)|reconfiguration|restoration|active distribution|virtual power plant|integrated energy system|energy hub|v2g|vehicle-to-grid|inverter|ieee 2030\.5'),
 'AMI & Consumer': has(r'smart meter|metering|\bami\b|electricity theft|energy theft|power theft|non-technical loss|load forecast|demand forecast|consumption forecast|residential|household|home energy|\bhems\b|building|consumer|customer load|demand response|prosumer|ev charging|electric vehicle charging|charging (?:station|demand|load)|load profil|non-intrusive|nilm'),
 'Billing, Market & Customer': has(r'billing|\bbill\b|bills|tariff|electricity pric|price forecast|electricity market|energy market|bidding|market clearing|energy trading|peer-to-peer|p2p energy|settlement|customer service|customer (?:query|queries|complaint|interaction|engagement|support)|call center|contract|retail|marketing|payment|power sales|electricity sales|user intent|question[- ]answering for (?:customer|user)')}
for k,v in seg.items(): E['seg_'+k]=v
E['seg_Cross-cutting']=~E[[c for c in E.columns if c.startswith('seg_')]].any(axis=1)
tech={
 'VQC/QNN': r'variational quantum|quantum neural|\bqnn|parametri[sz]ed quantum circuit|quantum convolutional|hybrid quantum[- ]classical (?:neural|network|model|deep)|quantum deep|dressed quantum|quantum autoencoder|quantum transformer|quantum classifier|quantum machine learning|\bqml\b',
 'Quantum kernel/QSVM': r'quantum kernel|qsvm|quantum support vector',
 'QLSTM/quantum RNN': r'(?<!quantile )qlstm|quantum long short|quantum (?:gated recurrent|gru|recurrent|lstm)|qgru',
 'Annealing/QAOA/QUBO': r'quantum annealing|annealer|qaoa|quantum approximate optimi|qubo|d-wave|ising|quantum optimi[sz]ation|benders|quantum surrogate',
 'Quantum linear/simulation': r'\bhhl\b|quantum linear|quantum power flow|quantum (?:emt|electromagnetic)|quantum state estimation|linear system(?:s)? of equations|quantum simulation|quantum contingency',
 'Quantum RL/FL': r'quantum reinforcement|quantum (?:deep )?q-|quantum federated|federated quantum|quantum multi-agent',
 'LLM general/fine-tuning': r'large language model|\bllms?\b|\bgpt|chatgpt|fine-tun|lora|instruction|deepseek|qwen|llama|large model',
 'RAG/knowledge QA': r'retrieval[- ]augmented|\brag\b|graphrag|knowledge (?:base|graph)|question[- ]answering|\bq&a\b',
 'LLM agents/multi-agent': r'\bagent|agentic|multi-agent|tool[- ]call|tool[- ]augmented|function call',
 'Time-series/foundation models': r'foundation model|time[- ]series foundation|timesfm|chronos|moirai|pre-?trained (?:time|model)',
 'Vision/multimodal LMs': r'vision[- ]language|multimodal large|multi-modal large|\bvlm|visual language|large vision|\bsam\b|segment anything|image',
 'Small/edge LMs': r'small language model|\bslms?\b|lightweight (?:large )?language|edge (?:llm|language)|on-device|quantiz|distill|tinyllm|small-large|large-small',
 'PQC (lattice/hash)': r'post[- ]quantum|lattice|kyber|ml-kem|dilithium|ml-dsa|sphincs|falcon|quantum[- ]resistant|quantum[- ]safe|ntru|lwe\b|mlwe',
 'QKD/QRNG': r'quantum key distribution|\bqkd|qrng|quantum random|bb84|quantum secure communication|quantum[- ]secured|quantum communication|semi-quantum|quantum key',
}
for k,p in tech.items(): E['t_'+k]=has(p)
E['fam_Q']=E.tech.str.contains('Q'); E['fam_L']=E.tech.str.contains('L'); E['fam_P']=E.tech.str.contains('P')
# family-gate subtypes
for k in ['VQC/QNN','Quantum kernel/QSVM','QLSTM/quantum RNN','Annealing/QAOA/QUBO','Quantum linear/simulation','Quantum RL/FL']: E['t_'+k]&=E.fam_Q
for k in ['LLM general/fine-tuning','RAG/knowledge QA','LLM agents/multi-agent','Time-series/foundation models','Vision/multimodal LMs','Small/edge LMs']: E['t_'+k]&=E.fam_L
for k in ['PQC (lattice/hash)','QKD/QRNG']: E['t_'+k]&=E.fam_P
E.to_pickle('prisma/eligible.pkl'); inc.to_pickle('prisma/screened_included.pkl')
P=E[~E.is_review]
print('eligible',len(E),'reviews',E.is_review.sum(),'primary',len(P))
print('families primary', P.fam_Q.sum(), P.fam_L.sum(), P.fam_P.sum(), 'Q&L',(P.fam_Q&P.fam_L).sum(),'Q&P',(P.fam_Q&P.fam_P).sum())
for c in [c for c in E.columns if c.startswith('seg_')]: print(c,P[c].sum())
for c in [c for c in E.columns if c.startswith('t_')]: print(c,P[c].sum())
print(P.year.value_counts().sort_index().to_dict())
print(P.pub.value_counts().to_dict())
