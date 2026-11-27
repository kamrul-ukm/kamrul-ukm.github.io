# INTERNATIONAL GUEST LECTURE: FEDERATED LEARNING

## Fundamentals & Architectures of Federated Learning
*From FedAvg to privacy-preserving, decentralized and foundation-model FL: theory, architectures, applications and code*

**Ts. Dr. Mohammad Kamrul Hasan**
Associate Professor · Head, Network and Communication Technology Lab
Centre for Cyber Security, Faculty of Information Science and Technology (FTSM), Universiti Kebangsaan Malaysia (UKM)
mkhasan@ukm.edu.my · hasankamrul@ieee.org · 27 November 2026

---

## Contents

| Folder | File | Description |
|---|---|---|
| `slides/` | [Federated-Learning-Talk-27November_2026.pdf](slides/Federated-Learning-Talk-27November_2026.pdf) | Lecture slides (68 pages) |
| `labs/` | [Lab1_Flower_PyTorch_Quickstart_10_Clients.ipynb](labs/Lab1_Flower_PyTorch_Quickstart_10_Clients.ipynb) | Lab 1: Flower PyTorch quickstart with 10 clients (FedAvg, IID) |
| `labs/` | [Lab2_Dirichlet_NonIID.ipynb](labs/Lab2_Dirichlet_NonIID.ipynb) | Lab 2: non-IID data with a Dirichlet α = 0.1 partition |
| `labs/` | [Lab3_FedAvg_vs_FedProx.ipynb](labs/Lab3_FedAvg_vs_FedProx.ipynb) | Lab 3: FedAvg vs FedProx (μ = 0.1, 0.5) over 30 rounds |
| `labs/` | [Lab4_DP_Clipping_Accuracy_Cost.ipynb](labs/Lab4_DP_Clipping_Accuracy_Cost.ipynb) | Lab 4: DP clipping and the accuracy cost of privacy |
| `labs/` | [FL_Labs_1-4_Complete_Solutions.ipynb](labs/FL_Labs_1-4_Complete_Solutions.ipynb) | All four labs with complete solutions in one notebook |

## Open the labs in Google Colab

| Lab | Open |
|---|---|
| Lab 1 · Quickstart with 10 clients | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kamrul-ukm/kamrul-ukm.github.io/blob/main/International-Guest-Lecture-Federated-Learning/labs/Lab1_Flower_PyTorch_Quickstart_10_Clients.ipynb) |
| Lab 2 · Dirichlet α = 0.1 (non-IID) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kamrul-ukm/kamrul-ukm.github.io/blob/main/International-Guest-Lecture-Federated-Learning/labs/Lab2_Dirichlet_NonIID.ipynb) |
| Lab 3 · FedAvg vs FedProx | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kamrul-ukm/kamrul-ukm.github.io/blob/main/International-Guest-Lecture-Federated-Learning/labs/Lab3_FedAvg_vs_FedProx.ipynb) |
| Lab 4 · DP clipping | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kamrul-ukm/kamrul-ukm.github.io/blob/main/International-Guest-Lecture-Federated-Learning/labs/Lab4_DP_Clipping_Accuracy_Cost.ipynb) |
| Labs 1–4 · Complete solutions | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kamrul-ukm/kamrul-ukm.github.io/blob/main/International-Guest-Lecture-Federated-Learning/labs/FL_Labs_1-4_Complete_Solutions.ipynb) |

**Tip:** in Colab choose *Runtime → Change runtime type → GPU*. Labs 2–4 run 30 rounds per experiment; set `QUICK_MODE = True` for a 10-round first pass.

## Lab exercises
1. Run the Flower PyTorch quickstart with 10 clients.
2. Switch to a Dirichlet α = 0.1 partition.
3. Compare FedAvg and FedProx (μ = 0.1, 0.5) over 30 rounds and plot accuracy.
4. Add DP clipping and report the accuracy cost.

## Requirements
- Python 3.10+, PyTorch and torchvision (preinstalled in Colab)
- `flwr[simulation]==1.44.0`, `flwr-datasets[vision]==0.6.1` (installed by the first cell of each notebook)
- Dataset: CIFAR-10, downloaded automatically via Flower Datasets

The notebooks use Flower's current Message API (`ClientApp` / `ServerApp` / `strategy.start`).

## Lecture outline
- **Part A · Fundamentals:** motivation, optimization objective and loss, FedAvg, worked tutorials, non-IID data, evaluation, poisoning, big picture
- **Part B · Architectures:** client–server, hierarchical (autonomous vehicles), peer-to-peer (V2V platoons, industrial IoT), blockchain-enabled, split learning
- **Part C · Advanced topics:** heterogeneity, communication efficiency, privacy and security, personalization, research frontiers
- **Part D · Applications & practice:** autonomous vehicles, healthcare, industrial IoT, smart grid; frameworks, Flower code, deployment, labs

## Citation
If you use these materials, please cite:
> Hasan, M. K. (2026). *Fundamentals & Architectures of Federated Learning*. International Guest Lecture, 27 November 2026. Universiti Kebangsaan Malaysia.
