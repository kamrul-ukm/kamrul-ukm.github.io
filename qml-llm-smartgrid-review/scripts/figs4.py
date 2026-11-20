import json, numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, Rectangle, FancyArrowPatch
from matplotlib.colors import LinearSegmentedColormap

# ---------- unified journal style ----------
NAVY, TEAL, AMBER, SLATE, RED, INK, GRID = "#1F3A5F", "#1A8C8C", "#E09F3E", "#5C6B7A", "#9E2A2B", "#1B1B1B", "#D9DEE5"
LT = {"navy": "#E6ECF3", "teal": "#E3F2F2", "amber": "#FBF0DF", "red": "#F6E3E3", "grey": "#F2F4F6"}
plt.rcParams.update({
    "font.family": "serif", "font.serif": ["Liberation Serif", "DejaVu Serif"], "mathtext.fontset": "stix",
    "font.size": 10, "axes.titlesize": 10.5, "axes.labelsize": 10, "xtick.labelsize": 9, "ytick.labelsize": 9,
    "legend.fontsize": 9, "axes.edgecolor": "#444", "axes.linewidth": 0.8, "savefig.dpi": 300,
})
c = json.load(open('prisma/counts_v3.json')); P = pd.read_pickle('prisma/v3_primary.pkl')

def node(ax, x, y, w, h, text, fc, ec, fs=9, bold=False, tc=INK, shape="round", lw=1.2):
    if shape == "round":
        ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.004,rounding_size=0.012", fc=fc, ec=ec, lw=lw, zorder=2))
    elif shape == "diamond":
        ax.add_patch(Polygon([(x, y + h/2), (x + w/2, y), (x, y - h/2), (x - w/2, y)], closed=True, fc=fc, ec=ec, lw=lw, zorder=2))
    elif shape == "para":
        s = 0.012
        ax.add_patch(Polygon([(x - w/2 + s, y + h/2), (x + w/2 + s, y + h/2), (x + w/2 - s, y - h/2), (x - w/2 - s, y - h/2)], closed=True, fc=fc, ec=ec, lw=lw, zorder=2))
    elif shape == "rect":
        ax.add_patch(Rectangle((x - w/2, y - h/2), w, h, fc=fc, ec=ec, lw=lw, zorder=2))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=tc, fontweight="bold" if bold else "normal", zorder=3, linespacing=1.25)

def step(ax, y, n, col):
    ax.plot(-0.025, y, 'o', ms=17, color=col, zorder=3); ax.text(-0.025, y, str(n), ha='center', va='center', color='white', fontsize=9, fontweight='bold', zorder=4)

def arrow(ax, p, q, color=SLATE, ls="-", lw=1.2, rad=0.0, text=None, tpos=0.5, toff=(0, 0), fs=8):
    a = FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=11, color=color, lw=lw, linestyle=ls,
                        connectionstyle=f"arc3,rad={rad}", zorder=1, shrinkA=2, shrinkB=2)
    ax.add_patch(a)
    if text:
        mx, my = p[0] + (q[0] - p[0]) * tpos + toff[0], p[1] + (q[1] - p[1]) * tpos + toff[1]
        ax.text(mx, my, text, fontsize=fs, color=color, ha="center", va="center", style="italic",
                bbox=dict(fc="white", ec="none", pad=0.6), zorder=4)

# =====================================================================
# Fig 1: PRISMA flow
# =====================================================================
fig, ax = plt.subplots(figsize=(8.2, 7.6)); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
stages = [("Identification", 0.80, 0.98), ("Screening", 0.52, 0.775), ("Eligibility", 0.29, 0.50), ("Included", 0.02, 0.27)]
for t, y0, y1 in stages:
    ax.add_patch(Rectangle((0, y0), 0.045, y1 - y0, fc=NAVY, ec="none"))
    ax.text(0.0225, (y0 + y1) / 2, t, rotation=90, ha="center", va="center", color="white", fontsize=9.5, fontweight="bold")
L, R, W = 0.30, 0.76, 0.40
node(ax, L, 0.89, W, 0.13, f"Records identified (20 November 2026)\nScopus  n = {c['scopus']:,}\nWeb of Science Core Collection  n = {c['wos']:,}\nTotal  n = {c['total']:,}", LT["navy"], NAVY)
node(ax, R, 0.89, 0.44, 0.13, f"Removed before screening\nCriterion 1 – Duplicate  n = {c['dup']:,}\n(within Scopus {c['dup_scopus']}; WoS–Scopus {c['dup_wos']:,})", LT["red"], RED)
s2 = c['nis']; pub = s2.get('Publisher outside IEEE/Elsevier/Springer/ACM/Wiley/MDPI', 0); yr = s2.get('Publication year outside 2018–2026', 0); topic = c['not_in_scope'] - pub - yr
node(ax, L, 0.64, W, 0.10, f"Records screened\n(title, abstract, keywords)\nn = {c['screened']:,}", LT["navy"], NAVY)
node(ax, R, 0.64, 0.44, 0.20, f"Excluded  n = {c['not_in_scope'] + c['incomplete']:,}\nCriterion 2 – Not in scope  n = {c['not_in_scope']:,}\n   publisher outside scope  {pub}\n   year outside 2018–2026  {yr}\n   topic / technique  {topic:,}\nCriterion 3 – Incomplete  n = {c['incomplete']}", LT["red"], RED, fs=8.6)
g = c['noexp_sub']; rv = g.get('Review / survey / perspective (no original experiment; used as background)', 0)
noexp = g.get('No experimental evaluation reported (conceptual / framework only)', 0) + g.get('Neither experimental evaluation nor grid data / test system reported', 0)
nogrid = g.get('No grid data, test system or grid scenario reported', 0)
node(ax, L, 0.395, W, 0.10, f"Records assessed for eligibility\nn = {c['assessed']:,}", LT["navy"], NAVY)
node(ax, R, 0.395, 0.44, 0.16, f"Criterion 4 – No experiment or no grid data\nn = {c['noexp']}\n   no experimental evaluation  {noexp}\n   no grid data / test system  {nogrid}\n   reviews / surveys (background)  {rv}", LT["red"], RED, fs=8.6)
node(ax, L, 0.145, W, 0.12, f"Studies included\nn = {c['included']:,}", LT["amber"], AMBER, fs=11, bold=True)
node(ax, R, 0.145, 0.44, 0.17, f"By technique family*\nQuantum ML / optimisation  {c['fam']['Q']}\nLanguage / foundation models  {c['fam']['L']}\nQuantum-safe security  {c['fam']['P']}\nQuantum + language model  4", LT["amber"], AMBER, fs=8.6)
for y1, y2 in [(0.825, 0.69), (0.59, 0.445), (0.345, 0.205)]: arrow(ax, (L, y1), (L, y2), NAVY)
for y in [0.89, 0.64, 0.395]: arrow(ax, (L + W/2, y), (R - 0.22, y), RED)
arrow(ax, (L + W/2, 0.145), (R - 0.22, 0.145), AMBER)
ax.text(0.06, 0.0, "*Families overlap; a study may belong to more than one.", fontsize=8, color=SLATE, style="italic")
plt.savefig("fig1_prisma.png", bbox_inches="tight"); plt.close()

# =====================================================================
# Fig 2: trends + publisher
# =====================================================================
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.5, 3.7), gridspec_kw={'width_ratios': [1.65, 1]})
yrs = list(range(2018, 2027)); x = np.arange(len(yrs))
q = [int(((P.year == y) & P.Qcore).sum()) for y in yrs]; l = [int(((P.year == y) & P.fam_L).sum()) for y in yrs]; p = [int(((P.year == y) & P.fam_P).sum()) for y in yrs]
a1.plot(x, l, "-o", color=TEAL, lw=2, ms=5, label="Language / foundation models")
a1.plot(x, q, "-s", color=AMBER, lw=2, ms=5, label="Quantum ML / optimisation")
a1.plot(x, p, "-^", color=NAVY, lw=2, ms=5, label="Quantum-safe security")
for series, col, dy in [(l, TEAL, 12), (q, AMBER, 12), (p, NAVY, -26)]:
    for xi, v in zip(x[-2:], series[-2:]): a1.annotate(str(v), (xi, v), textcoords="offset points", xytext=(0, 6 if dy > 0 else -13), ha="center", fontsize=8, color=col)
a1.set_xticks(x); a1.set_xticklabels(yrs); a1.set_ylabel("Included studies"); a1.grid(axis="y", color=GRID, lw=0.7); a1.set_axisbelow(True)
a1.spines[['top', 'right']].set_visible(False); a1.legend(frameon=False, loc="upper left")
a1.axvspan(7.5, 8.5, color=LT["grey"], zorder=0); a1.text(8, max(l) * 0.55, "partial\nyear", ha="center", fontsize=7.5, color=SLATE, style="italic")
a1.set_title("(a) Annual output by technique family", loc="left", color=NAVY)
pub = P.pub.replace({'Springer Nature': 'Springer', 'Springer (BMC)': 'Springer', 'Wiley (IET)': 'Wiley', 'Wiley (Hindawi)': 'Wiley'}).value_counts()
cols = [NAVY, TEAL, AMBER, "#4F7CAC", SLATE, "#B5651D"][:len(pub)]
a2.barh(pub.index[::-1], pub.values[::-1], color=cols[::-1], height=0.62)
for i, v in enumerate(pub.values[::-1]): a2.text(v + 10, i, f"{v}  ({100 * v / len(P):.0f}%)", va="center", fontsize=8.5)
a2.set_xlim(0, pub.max() * 1.38); a2.spines[['top', 'right']].set_visible(False); a2.grid(axis="x", color=GRID, lw=0.7); a2.set_axisbelow(True)
a2.set_xlabel("Included studies"); a2.set_title("(b) Distribution by publisher", loc="left", color=NAVY)
plt.tight_layout(); plt.savefig("fig3_trends.png", bbox_inches="tight"); plt.close()

# =====================================================================
# Fig 3: evidence-map heatmap
# =====================================================================
segs = ['Generation', 'Transmission', 'Distribution & DER', 'AMI & Consumer', 'Billing, Market & Customer', 'Cross-cutting']
techs = ['VQC/QNN', 'Quantum kernel/QSVM', 'QLSTM/quantum RNN', 'Annealing/QAOA/QUBO', 'Quantum linear/simulation', 'Quantum RL/FL', 'LLM general/fine-tuning', 'RAG/knowledge QA', 'LLM agents/multi-agent', 'Time-series/foundation models', 'Vision/multimodal LMs', 'Small/edge LMs', 'PQC (lattice/hash)', 'QKD/QRNG']
lab = ['VQC /\nQNN', 'Kernel /\nQSVM', 'QLSTM /\nQ-RNN', 'Annealing /\nQAOA', 'Linear /\nsimulation', 'Quantum\nRL / FL', 'LLM /\nfine-tune', 'RAG /\nKG-QA', 'Agents /\nmulti-agent', 'Time-series\nFM', 'Vision /\nmultimodal', 'Small /\nedge LM', 'PQC', 'QKD /\nQRNG']
M = np.array([[int((P['seg_' + s] & P['t_' + t]).sum()) for t in techs] for s in segs])
fig, ax = plt.subplots(figsize=(11.8, 4.3))
cm = LinearSegmentedColormap.from_list("nt", ["#FFFFFF", "#CFE8E8", TEAL, NAVY])
im = ax.imshow(np.log1p(M), cmap=cm, aspect="auto")
ax.set_xticks(range(len(techs))); ax.set_xticklabels(lab, fontsize=8.3); ax.set_yticks(range(len(segs))); ax.set_yticklabels(segs, fontsize=9.3)
ax.set_xticks(np.arange(-.5, len(techs)), minor=True); ax.set_yticks(np.arange(-.5, len(segs)), minor=True)
ax.grid(which="minor", color="white", lw=1.6); ax.tick_params(which="minor", length=0); ax.tick_params(length=0)
for sp in ax.spines.values(): sp.set_visible(False)
for i in range(len(segs)):
    for j in range(len(techs)):
        v = M[i, j]; ax.text(j, i, v if v else "·", ha="center", va="center", color="white" if v >= 35 else INK, fontsize=9.5, fontweight="bold" if v >= 35 else "normal")
for xv in [5.5, 11.5]: ax.axvline(xv, color=AMBER, lw=2.2)
for xc, t in [(2.5, "Quantum ML / optimisation"), (8.5, "Language / foundation models"), (12.5, "Quantum-safe")]:
    ax.text(xc, -0.85, t, ha="center", va="bottom", fontsize=9.5, color=NAVY, fontweight="bold")
cb = plt.colorbar(im, ax=ax, fraction=0.02, pad=0.01); cb.set_ticks(np.log1p([0, 5, 20, 50, 150])); cb.set_ticklabels(["0", "5", "20", "50", "150"]); cb.outline.set_visible(False); cb.ax.tick_params(labelsize=8)
plt.savefig("fig4_heatmap.png", bbox_inches="tight"); plt.close()

# =====================================================================
# Fig 4: proposed framework as a flowchart
# =====================================================================
fig, ax = plt.subplots(figsize=(10.8, 10.2)); ax.set_xlim(-0.05, 1.0); ax.set_ylim(0, 1.0); ax.axis("off")
# security side-band
ax.add_patch(FancyBboxPatch((0.925, 0.03), 0.06, 0.94, boxstyle="round,pad=0.004,rounding_size=0.015", fc=LT["red"], ec=RED, lw=1.2))
ax.text(0.955, 0.50, "Quantum-safe security & governance:  NIST PQC (ML-KEM / ML-DSA)  ·  QKD  ·  IEC 62351  ·  NISTIR 7628  ·  audit",
        rotation=90, ha="center", va="center", fontsize=8.6, color=RED, fontweight="bold")
# (1) sources
segs5 = [("Generation", "unit controllers, PV/wind\ninverters, plant PMUs"), ("Transmission", "PMUs/PDCs, IEDs,\nRTUs, EMS/SCADA"),
         ("Distribution & DER", "feeder IEDs, DERMS,\nBESS, EV chargers"), ("AMI & Consumer", "smart meters, data\nconcentrators, HEMS"),
         ("Billing & Market", "MDMS, CIS / billing,\nmarket platform")]
xs = np.linspace(0.10, 0.82, 5); ytop = 0.925
for (t, d), xx in zip(segs5, xs):
    node(ax, xx, ytop + 0.018, 0.155, 0.04, t, NAVY, NAVY, fs=9, bold=True, tc="white", shape="rect")
    node(ax, xx, ytop - 0.022, 0.155, 0.045, d, LT["navy"], NAVY, fs=8.2, shape="rect")
step(ax, ytop, 1, NAVY)
# (2) ingestion
node(ax, 0.46, 0.80, 0.80, 0.055, "Protocol ingestion:  IEC 61850 (GOOSE/SV/MMS) · DNP3 · IEEE C37.118 · IEEE 2030.5 · DLMS/COSEM · OpenADR · CIM", LT["teal"], TEAL, fs=8.5, shape="para")
step(ax, 0.80, 2, TEAL)
for xx in xs: arrow(ax, (xx, ytop - 0.0425), (xx if abs(xx - 0.46) < 0.01 else xx * 0.9 + 0.046, 0.828), SLATE)
# (3) data fabric
node(ax, 0.46, 0.705, 0.80, 0.06, "Edge–fog–cloud data fabric:  historians · feature stores · grid digital twin · federated aggregation (privacy-preserving)", LT["grey"], SLATE, fs=9)
step(ax, 0.705, 3, SLATE)
arrow(ax, (0.46, 0.7725), (0.46, 0.735), SLATE)
# (4) decision
node(ax, 0.46, 0.585, 0.30, 0.11, "Task\nclassification", "white", NAVY, fs=9.5, bold=True, shape="diamond")
step(ax, 0.585, 4, NAVY)
arrow(ax, (0.46, 0.675), (0.46, 0.640), SLATE)
# branches
node(ax, 0.15, 0.43, 0.24, 0.10, "Language-model planner\ncloud LLM or edge SLM\nRAG over standards & tariffs\ntool-calling agent", LT["teal"], TEAL, fs=8.6)
node(ax, 0.46, 0.43, 0.24, 0.10, "Quantum solver / QML\nQAOA · annealing (QUBO)\nVQC / QNN · quantum kernel\nQLSTM forecasting", LT["amber"], AMBER, fs=8.6)
node(ax, 0.77, 0.43, 0.24, 0.10, "Classical edge controller\nprotection & real-time control\n(< 10 ms deadline;\nquantum / LLM not used)", LT["grey"], SLATE, fs=8.6)
arrow(ax, (0.31, 0.585), (0.15, 0.48), TEAL, text="query, explanation,\nplanning", tpos=0.45, toff=(-0.04, 0.02))
arrow(ax, (0.46, 0.53), (0.46, 0.48), AMBER, text="combinatorial / learning", tpos=0.5, toff=(0.10, 0.0))
arrow(ax, (0.61, 0.585), (0.77, 0.48), SLATE, text="time-critical", tpos=0.45, toff=(0.05, 0.02))
arrow(ax, (0.27, 0.445), (0.34, 0.445), TEAL, ls="--", text="calls as tool", tpos=0.5, toff=(0, 0.03))
arrow(ax, (0.34, 0.415), (0.27, 0.415), AMBER, ls="--", text="result", tpos=0.5, toff=(0, -0.018))
# (5) verification
node(ax, 0.30, 0.275, 0.30, 0.11, "Classical verifier\nphysics & tariff\nconstraints met?", "white", NAVY, fs=9, bold=True, shape="diamond")
step(ax, 0.275, 5, NAVY)
arrow(ax, (0.15, 0.38), (0.24, 0.31), TEAL); arrow(ax, (0.46, 0.38), (0.36, 0.31), AMBER)
ax.plot([0.15, 0.06], [0.275, 0.275], color=RED, lw=1.2, zorder=1)
arrow(ax, (0.06, 0.275), (0.06, 0.38), RED)
ax.text(0.05, 0.33, "no: re-plan", rotation=90, fontsize=8, color=RED, style="italic", va="center", ha="right")
# (6) outputs
outs = ["UC & dispatch\nschedule", "stability &\nsecurity alerts", "DER / volt-VAR\nset-points", "theft flags &\nload forecasts", "certified bill +\nLLM explanation"]
ox = np.linspace(0.10, 0.82, 5)
node(ax, 0.46, 0.155, 0.80, 0.045, "Human-in-the-loop approval and deterministic execution (bill computed from certified meter data)", LT["navy"], NAVY, fs=9)
arrow(ax, (0.30, 0.22), (0.30, 0.178), NAVY, text="yes", tpos=0.45, toff=(0.025, 0))
arrow(ax, (0.77, 0.38), (0.77, 0.178), SLATE)
step(ax, 0.155, 6, NAVY)
for xx, t in zip(ox, outs):
    node(ax, xx, 0.065, 0.155, 0.07, t, LT["amber"], AMBER, fs=8.6)
    arrow(ax, (xx if abs(xx - 0.46) < 0.01 else xx * 0.9 + 0.046, 0.1325), (xx, 0.1), SLATE)
step(ax, 0.065, 7, AMBER)
plt.savefig("fig1_architecture.png", bbox_inches="tight"); plt.close()

# =====================================================================
# Fig 5: roadmap as a timeline
# =====================================================================
fig, ax = plt.subplots(figsize=(10.5, 4.6)); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
ax.add_patch(FancyArrowPatch((0.02, 0.83), (0.99, 0.83), arrowstyle="-|>", mutation_scale=18, color=SLATE, lw=2.2))
phases = [("Near term  2026–2028", "NISQ + quantum-inspired", TEAL, LT["teal"],
           ["PQC (ML-KEM / ML-DSA) in DLMS/COSEM and IEEE 2030.5 meters", "Hybrid QLSTM / QNN heads on classical forecasters", "LLM copilots and edge SLMs with RAG over standards and tariffs", "Open benchmarks with parameter-matched baselines"]),
          ("Mid term  2028–2031", "early fault-tolerant", "#4F7CAC", "#E7EEF6",
           ["QAOA / annealing UC and DER dispatch in market sandboxes", "Federated QML across utilities with differential privacy", "LLM agents calling quantum optimisers as verified tools", "QKD trusted-node backbones on OPGW fibre"]),
          ("Long term  2031+", "fault-tolerant QPU", NAVY, LT["navy"],
           ["Quantum-accelerated SCOPF and TSA in control rooms", "End-to-end generation-to-billing quantum–LM digital twin", "Certified, explainable quantum billing analytics", "Standards for quantum and generative AI in grid operations"])]
for k, (t, sub, col, fc, items) in enumerate(phases):
    x0 = 0.02 + k * 0.33
    ax.plot(x0 + 0.155, 0.83, 'o', ms=13, color=col, zorder=3)
    ax.text(x0 + 0.155, 0.93, t, ha="center", fontsize=10.5, fontweight="bold", color=col)
    ax.text(x0 + 0.155, 0.885, sub, ha="center", fontsize=9, style="italic", color=SLATE)
    ax.add_patch(FancyBboxPatch((x0, 0.04), 0.31, 0.72, boxstyle="round,pad=0.004,rounding_size=0.015", fc=fc, ec=col, lw=1.2))
    for j, it in enumerate(items):
        y = 0.67 - j * 0.165
        ax.plot(x0 + 0.03, y, 'o', ms=14, color=col); ax.text(x0 + 0.03, y, str(j + 1), ha="center", va="center", color="white", fontsize=8.5, fontweight="bold")
        import textwrap
        ax.text(x0 + 0.055, y, "\n".join(textwrap.wrap(it, 33)), va="center", fontsize=8.8, color=INK)
plt.savefig("fig4_roadmap.png", bbox_inches="tight"); plt.close()
print("done")
