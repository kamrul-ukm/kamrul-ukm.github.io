import pandas as pd, re
U=pd.read_pickle('prisma/unique_pub.pkl'); X=U[U.pub_ok].copy()
def low(*c): return ' '.join(str(x) for x in c if isinstance(x,str)).lower()
X['ta']=X.apply(lambda r: low(r['title'],r['abstract']),axis=1)
X['tk']=X.apply(lambda r: low(r['title'],r['keywords']),axis=1)
R=lambda p: re.compile(p)
Q_STRONG=R(r'qubit|quantum circuit|variational quantum|quantum neural|quantum kernel|qsvm|(?<!quantile )qlstm|quantum long short|quantum annealing|quantum annealer|annealer|qaoa|quantum approximate optimi|qubo|d-wave|dwave|\bhhl\b|quantum machine learning|\bqml\b|quantum computer|ibm quantum|pennylane|qiskit|quantum processor|quantum hardware|\bnisq\b|quantum reinforcement|quantum convolutional|quantum federated|quantum autoencoder|quantum transformer|quantum generative|quantum boltzmann|quantum support vector|quantum-classical|quantum classical|quantum classifier|quantum feature|quantum embedding|quantum optimi[sz]ation|quantum linear|quantum power flow|quantum state estimation')
Q_WEAK=R(r'quantum computing|quantum algorithm|quantum-enhanced|quantum enhanced|quantum technolog|quantum advantage|quantum speed')
Q_INSP=R(r'quantum[- ]inspired|quantum[- ]behaved|quantum particle swarm|\bqpso\b|quantum genetic|quantum evolutionary|quantum[- ]based (?:particle|genetic|dragonfly)|quantum immune|quantum firefly|quantum whale|quantum chaotic|quantum harmony')
L=R(r'large language model|\bllms?\b|\bgpt[- ]?\d*|chatgpt|foundation model|retrieval[- ]augmented|small language model|language model|generative pre-?trained|\bcopilot|\bbert\b|llama|qwen|deepseek|vision[- ]language|multimodal large|prompt engineering|in-context learning|agentic|\bai agent|llm[- ]based|instruction[- ]tun')
L_NOISE=R(r'spatial light modulat|laser melting|selective laser|\bslms\b|\bnlms\b')
Q_NOISE=R(r'\bqca\b|quantum[- ]dot|quantum efficienc|quantum well|quantum yield|quantum chemistry|quantum material|perovskite|solar cell|interatomic|entanglement[- ]distribution network')
PQ=R(r'post[- ]quantum|quantum[- ]safe|quantum[- ]resistant|quantum[- ]secure|quantum key distribution|\bqkd\b|kyber|ml-kem|dilithium|ml-dsa|lattice[- ]based|quantum random number|\bqrng\b|quantum cryptograph|quantum attack|quantum threat|harvest[- ]now')
DOM=R(r'smart grid|power system|power grid|electric(?:al|ity)? grid|electricity|power distribution|distribution network|distribution grid|transmission (?:line|system|network|grid)|microgrid|micro-grid|unit commitment|economic dispatch|optimal power flow|power flow|demand response|load forecast|smart meter|metering|advanced metering|\bami\b|substation|\bscada\b|photovoltaic power|pv power|pv generation|pv system|wind power|wind farm|wind turbine|solar power|renewable energ|energy management system|\bhems\b|energy storage|battery energy storage|distributed energy|\bders?\b|ev charging|electric vehicle charging|vehicle-to-grid|\bv2g\b|tariff|billing|electricity market|energy market|energy trading|peer-to-peer energy|virtual power plant|state estimation|transient stability|voltage stability|frequency regulation|power plant|hydropower|nuclear power|energy theft|electricity theft|power theft|iec 61850|dnp3|synchrophasor|\bpmu|grid operator|electric utilit|power utilit|prosumer|power dispatch|dispatching|power load|power equipment|power transformer|transmission line|overhead line|power outage|power supply|electric power|energy internet|integrated energy system|load profil|power engineering|power and energy|transformer fault|transformer health|power monitoring|energy infrastructure|building energy|electrical equipment|insulator|transmission tower|power inspection|energy management|power quality|grid-connected|energy communit|charging station|power converter|inverter')
AI_ENERGY=R(r'energy consumption of (?:llm|ai|large language|model)|energy efficien\w* (?:of|for) (?:llm|inference|training)|carbon footprint of|green ai|inference energy|training energy|energy cost of (?:llm|ai)')
def classify(r):
    ta,tk=r['ta'],r['tk']
    ta_q=re.sub(r'quantile[- ]?(?:lstm|long short-term memory)|\(qlstm\)','',ta) if 'quantile' in ta else ta
    qs=bool(Q_STRONG.search(ta_q)); qw=bool(Q_WEAK.search(ta)); qi=bool(Q_INSP.search(ta))
    l=bool(L.search(ta)) and not (L_NOISE.search(ta) and not re.search(r'language model',ta))
    p=bool(PQ.search(ta)); d=bool(DOM.search(ta))
    q = qs or (qw and not qi)
    if (Q_INSP.search(str(r['title']).lower()) or re.search(r'quantum[- ]enhanced (?:mfo|pso|grey|whale|firefly|genetic)',ta)) and not re.search(r'qubit|quantum circuit|annealer|quantum annealing|qaoa|quantum hardware|quantum computer',ta): q=False
    tech=[]; 
    if q: tech.append('Q')
    if l: tech.append('L')
    if p: tech.append('P')
    if not tech:
        if qi: return 'EC1: quantum-inspired metaheuristic only',''
        if L_NOISE.search(ta): return 'EC1: SLM = spatial light modulator / laser melting',''
        return 'EC4: no QML / LM / quantum-safe technique in title-abstract',''
    dt=bool(DOM.search(tk)); dn=len(DOM.findall(ta))
    if not d or (not dt and dn<2): return 'EC5: not a smart-grid / power-system application',''.join(tech)
    if Q_NOISE.search(ta) and not (l or p or re.search(r'qubit|quantum circuit|quantum comput|quantum annealing|qaoa|quantum neural|quantum machine',ta)): return 'EC1: quantum materials / devices, not quantum computing',''.join(tech)
    if re.search(r'water distribution|power divider|antenna|bill of materials|\bbom\b',ta) and not re.search(r'smart grid|power grid|electric',str(r['title']).lower()): return 'EC5: not a smart-grid / power-system application',''.join(tech)
    if AI_ENERGY.search(ta) and not re.search(r'grid|demand response|power system',ta): return 'EC5: energy footprint of AI, not grid application',''.join(tech)
    # technique must be central: in title/keywords or >=2 mentions in abstract
    cnt=len(Q_STRONG.findall(ta))+len(Q_WEAK.findall(ta))+len(L.findall(ta))+len(PQ.findall(ta))
    intitle=bool(Q_STRONG.search(tk) or Q_WEAK.search(tk) or L.search(tk) or PQ.search(tk))
    if not intitle and cnt<2: return 'EC6: technique peripheral (single passing mention)',''.join(tech)
    ab=str(r['abstract']) if isinstance(r['abstract'],str) else ''
    if len(ab)<300: return 'EC7: no / insufficient abstract for appraisal',''.join(tech)
    return 'INCLUDE',''.join(tech)
res=X.apply(classify,axis=1,result_type='expand'); X['decision']=res[0]; X['tech']=res[1]
print(X['decision'].value_counts().to_dict())
inc=X[X.decision=='INCLUDE']; print(inc['tech'].value_counts().to_dict())
print(inc['doctype'].value_counts().to_dict())
X.to_pickle('prisma/screen1.pkl')
