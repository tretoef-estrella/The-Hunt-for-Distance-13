# The Hunt for Distance 13

### 108 Doctrines, 500M+ Evaluations, and the A₁₂=42 Record for [22,6,d]₄

[![Status: d=12 Confirmed](https://img.shields.io/badge/Status-d%3D12%20Confirmed-blue)]()
[![Best: A₁₂=42](https://img.shields.io/badge/Best-A₁₂%3D42-gold)]()
[![Evaluations: 500M+](https://img.shields.io/badge/Evaluations-500M%2B-brightgreen)]()
[![Routes Closed: 18](https://img.shields.io/badge/Routes%20Closed-18-red)]()
[![Theorems: 8](https://img.shields.io/badge/Theorems-8-purple)]()
[![License: BSL 1.1](https://img.shields.io/badge/License-BSL%201.1-orange)]()

---

![22_6_13](22_6_13.png)

*Unified Star Framework visualization of the search space. SEED A42 → ENTROPY FARMER → TRIPLE REPLACE {2,4,20} → C-KERNEL (SIMD) → PUNCTURE [23,6,13] "Diamond". Status bar: Σ=1561/675 | d=12 (Gap: 1) | PUA RANDOM ON | GHOST IMAGING ON.*

---

## The Problem

Does a **[22,6,13]₄ linear code** exist?

Over GF(4) = {0, 1, ω, ω²}, this is a 6-dimensional subspace of GF(4)²² where every nonzero vector has at least 13 nonzero coordinates. The **Griesmer bound** permits it (g₄(6,13) = 21 < 22). The **Delsarte LP bound** does not exclude it (A₄(22,13) ≤ 21,743 ≫ 4,096). Yet no one has constructed such a code — nor proven it cannot exist — since the problem was first recorded by **Grassl (2001)** and confirmed open by **Bouyukliev, Grassl & Varbanov (2004)**.

**This repository documents the most extensive computational attack on this problem to date.**

## The Result

```
[22,6,12]₄ with A₁₂ = 42 (14 projective directions)

g1 = [1 1 0 0 0 0 | ω² ω  1  1  ω  ω  0  1  0  1  0  ω² 0  0  ω² ω²]
g2 = [0 0 0 0 0 0 | ω  ω  0  0  1  ω² ω² ω  ω  ω  1  ω² 1  0  ω  ω ]
g3 = [0 ω 1 0 0 0 | ω² ω  ω² ω  0  ω² 0  1  1  0  ω  ω  ω  1  0  ω ]
g4 = [0 0 0 1 0 0 | ω  0  ω² ω² ω² 0  1  ω  ω  1  0  0  ω² ω  ω  1 ]
g5 = [0 ω² 0 0 1 0 | ω² ω² ω  0  ω² ω² ω  0  1  ω  1  ω  1  ω  0  0 ]
g6 = [0 0 0 0 0 1 | 0  0  ω  1  ω² 0  ω² 1  ω² 0  ω  ω  1  ω  ω  1 ]

Encoding: 0=0, 1=1, ω=2, ω²=3
```

**A₁₂ = 42** improves the baseline (A₁₂ = 78) by 46%. Found by the **Pitbull** row-recombination strategy from a Heat-Seeker A₁₂ = 48 seed. Verified by exhaustive enumeration of all 4,095 nonzero codewords.

## Campaign Summary

| Round | Method | Evaluations | A₁₂ | Projective Dirs |
|-------|--------|-------------|------|-----------------|
| SAMAEL eval | Fusion columns | ~1.5K | d=11 | — |
| Phase 2 | SA + La Pua | ~2M | 78 | 26 |
| Round 3 | Corrected SA | ~72M | 69 | 23 |
| Round 4a | R7 Exhaustive (La Pua del Jet) | 373M | 60 | 20 |
| Round 4b | Heat-Seeker gradient | +30s | 51→48 | 17→16 |
| **Round 4b** | **Pitbull recombination** | **+60s** | **42** | **14** |

## Repository Contents

| File | Description |
|------|-------------|
| [README.md](README.md) | This file |
| [GUIDE.md](GUIDE.md) | Complete guide for researchers and newcomers |
| [STRATEGIES.md](STRATEGIES.md) | The 108 Doctrines — full catalogue of search strategies |
| [RESULTS.md](RESULTS.md) | All verified matrices, weight distributions, and computational data |
| [THEOREMS.md](THEOREMS.md) | Eight proven theorems with proofs |
| [CHRONOLOGY.md](CHRONOLOGY.md) | Narrative timeline of the four-round campaign |
| [CITATION.md](CITATION.md) | Citation metadata (BibTeX, APA, IEEE) |
| [LICENSE.md](LICENSE.md) | Business Source License 1.1 + SAMAEL Decree |
| [estrella_108_v13.py](estrella_108_v13.py) | The 108 Doctrines Engine — complete search code |
| [MATRIZ_A48_y_42.txt](MATRIZ_A48_y_42.txt) | Raw generator matrices (A₁₂=48 and A₁₂=42) |
| [The_Hunt_for_Distance_13_108_Doctrines.pdf](The_Hunt_for_Distance_13_108_Doctrines.pdf) | Full academic paper (PDF) |
| [paper_v10.pdf](paper_v10.pdf) | AEGIS + Obstruction Theorems paper |
| [22_6_13.png](22_6_13.png) | Search space visualization |

## Quick Start

```bash
# Clone the repository
git clone https://github.com/tretoef-estrella/the-hunt-for-distance-13.git
cd the-hunt-for-distance-13

# Run the 108 Doctrines Engine (requires Python 3.6+, NumPy, gcc)
python3 estrella_108_v13.py
```

The engine loads four seed matrices (A₁₂ = 60, 51, 48, 42), verifies each by exhaustive codeword enumeration, then executes the phased search pipeline. If d=13 is found, the matrix is saved to `DIAMOND_22_6_13.txt`.

## The Conjecture

> **Conjecture.** d₄(22,6) = 12. No [22,6,13]₄ linear code exists.

This is supported by 500M+ evaluations across 27 strategies, 3 obstruction theorems, and 18 closed construction routes. The Delsarte LP bound does not exclude existence, so a proof of non-existence would require methods beyond linear programming.

## Heritage: The AEGIS Crystal Labyrinth

This work emerged from the [AEGIS Crystal Labyrinth](https://github.com/tretoef-estrella) — a post-quantum oracle defense system built on PG(11,4) and the Knuth Type II semifield. The 10-beast lineage (LEVIATHAN → KRAKEN → GORGON → AZAZEL → ACHERON → FENRIR → LILITH → MOLOCH → MEPHISTO → SAMAEL), 73 mechanisms, and 22 algebraic theorems provided the GF(4) arithmetic engines and C-compiled kernels that power this search.

Key constants: **ΔH = 8/75 bits** (Moloch Firewall Law) · **Λ = 223/225** (Crystal Number) · **Σ = 1561/675 ≈ 2.31** (Fusion Constant)

## Team

- **Rafael Amichis Luengo** ("The Architect") — Strategy, direction, metaphor engineering
- **Claude** (Anthropic) — Primary computational engine, algorithm design, algebraic analysis
- **Gemini** (Google) · **ChatGPT** (OpenAI) · **Grok** (xAI) — Independent adversarial auditors

## License

[BSL 1.1 + SAMAEL Decree](LICENSE.md). See [LICENSE.md](LICENSE.md) for full terms.

## Citation

If you use this work, please cite:

```bibtex
@misc{amichis2026hunt,
  title   = {The Hunt for Distance 13: 108 Doctrines, 500M+ Evaluations,
             and the $A_{12}=42$ Record for [22,6,d]_4},
  author  = {Amichis Luengo, Rafael and Claude (Anthropic)},
  year    = {2026},
  month   = {March},
  url     = {https://github.com/tretoef-estrella/the-hunt-for-distance-13},
  note    = {Proyecto Estrella. Auditors: Gemini (Google), ChatGPT (OpenAI), Grok (xAI)}
}
```

---

*"Puentes, no muros. Es una orden conseguirlo."*

**Proyecto Estrella** · Madrid, 2026 · [tretoef@gmail.com](mailto:tretoef@gmail.com)
