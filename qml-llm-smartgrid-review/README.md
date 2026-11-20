# Supplementary Data — Quantum Machine Learning with LLMs in Smart Grid Generation to Consumer Billing

Supplementary material for the systematic review:

> **A Systematic Review of Quantum Machine Learning with Large Language Models in Smart Grid Generation to Consumer Billing: Algorithms, Constraints, and Future Recommendations**
> Mohammad Kamrul Hasan *et al.* — Universiti Kebangsaan Malaysia (UKM). Manuscript submitted to *Artificial Intelligence Review* (Springer).

## Contents

| File | Description |
|---|---|
| `Supplementary_Tables_S1-S4_QML_LLM_SmartGrid.xlsx` | Supplementary Tables S1–S4 (see below) |
| `search_strings_scopus_wos.txt` | Full Scopus and Web of Science Core Collection search strings (run 20 November 2026) |
| `scripts/` | Python scripts used for merging, de-duplication, screening, eligibility assessment, coding, and figure generation |

### Supplementary Tables

| Sheet | Content | Rows |
|---|---|---|
| **S1 Included studies** | All included studies with ID (S0001–S1299), author–year citation, authors, year, title, venue, publisher, document type, DOI, value-chain segment(s), technique family, technique sub-type(s), citation count, and whether the study is cited in the main text | 1,299 |
| **S2 Screening log** | Every identified record with its exclusion criterion and reason, or "Included" | 4,569 |
| **S3 PRISMA counts** | Counts for each stage of the PRISMA 2020 flow diagram | 24 |
| **S4 Coding matrix** | Binary (TRUE/FALSE) coding of technique family, six value-chain segments, and 14 technique sub-types for all included studies | 1,299 |

## PRISMA 2020 summary

| Stage | n |
|---|---|
| Records identified — Scopus | 2,784 |
| Records identified — Web of Science Core Collection | 1,785 |
| **Total identified** | **4,569** |
| Criterion 1 — Duplicate (removed before screening) | 1,638 |
| Records screened | 2,931 |
| Criterion 2 — Not in scope | 1,448 |
| Criterion 3 — Incomplete | 5 |
| Records assessed for eligibility | 1,478 |
| Criterion 4 — No experiment or no grid data | 179 |
| **Studies included** | **1,299** |

### Exclusion criteria

1. **Duplicate** — same DOI or normalised title as an earlier record.
2. **Not in scope** — publisher outside IEEE, Elsevier, Springer, ACM, Wiley, or MDPI; publication year outside 2018–2026; not a power-system / smart-grid application; no QML, quantum-optimisation, language-model, or quantum-safe technique; quantum-inspired heuristics only; technique not central; AI/LLM treated only as an electrical load.
3. **Incomplete** — missing or insufficient abstract, missing bibliographic fields, or retracted record.
4. **No experiment or no grid data** — no experimental evaluation, no grid data / test system, or review/survey without original experiments.

## Value-chain segments and techniques

- **Segments:** Generation; Transmission; Distribution & DER; AMI & Consumer; Billing, Market & Customer; Cross-cutting.
- **Quantum ML / optimisation:** VQC/QNN, quantum kernel/QSVM, QLSTM/quantum RNN, annealing/QAOA/QUBO, quantum linear solvers/simulation, quantum RL/FL.
- **Language / foundation models:** LLM use/fine-tuning, RAG/knowledge QA, LLM agents/multi-agent, time-series foundation models, vision/multimodal LMs, small/edge LMs.
- **Quantum-safe security:** post-quantum cryptography (lattice/hash-based), QKD/QRNG.

## Method note

Title, abstract, and keyword screening was carried out with documented rule-based scripts (`scripts/`) and validated manually on a random sample of 100 records (91% correct). Eligibility was judged on titles, abstracts, and keywords. Bibliographic data are reproduced from Scopus and Web of Science exports.

## Citation

If you use this dataset, please cite the article above (citation details will be added on publication).

## Contact

Dr. Mohammad Kamrul Hasan — Network and Communication Technology Lab, Centre for Cyber Security, Faculty of Information Science and Technology, Universiti Kebangsaan Malaysia — mkhasan@ukm.edu.my
