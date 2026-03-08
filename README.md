# The Hunt for Distance 13

![Status](https://img.shields.io/badge/Status-d%3D12%20Confirmed-blue)
![Record](https://img.shields.io/badge/World%20Record-A%E2%82%81%E2%82%82%3D33-gold)
![Evaluations](https://img.shields.io/badge/Evaluations-1.4B%2B-brightgreen)
![Routes Closed](https://img.shields.io/badge/Routes%20Closed-24%2B-red)
![Theorems](https://img.shields.io/badge/Theorems-6-purple)
![License](https://img.shields.io/badge/License-CC%20BY%204.0-orange)

**A computational campaign targeting the open problem d₄(22,6) = 12 or 13**

> *"The entry has listed the range 12–13 since 2001."*
> — Grassl, codetables.de [accessed March 2026]

Twenty-four years. No movement.

This repository documents an independent research campaign that reduced the minimum number of weight-12 codewords in a [22,6,12]₄ linear code over GF(4) from **A₁₂ = 78** (prior baseline) to the current world record of **A₁₂ = 33** — achieved March 2026, without institutional affiliation or funding.

---

## The Result

There exists a **[22,6,12]₄ linear code** over GF(4) with **A₁₂ = 33** (11 projective directions in PG(5,4)).

The generator matrix is explicit, public, and verifiable in under one second on any modern CPU by exhaustive enumeration of all 4,095 nonzero codewords. No specialized software required.

```
     1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20  21  22
g1 [ 0   w2  0   w   0   0   1   0   w   1   1   0   0   0   1   0   w2  1   1   w2  w2  w2 ]
g2 [ w   w   1   1   1   w2  w2  0   w2  w   1   0   w   0   w   1   0   w   w2  w   1   0  ]
g3 [ w2  1   1   w   w2  1   0   1   w2  1   w2  w   0   0   0   0   w   0   1   w   1   0  ]
g4 [ 0   w2  w2  w2  1   w   w   1   0   w   0   0   0   w2  w2  w   w   1   w2  w2  0   0  ]
g5 [ w   0   w   0   w2  w2  w   w   w2  0   w2  0   0   0   w2  w2  1   w   1   w   1   0  ]
g6 [ w2  0   0   w2  w   w2  w   w   w   1   w2  0   0   0   w   1   1   0   0   0   0   0  ]

GF(4): 0=0, 1=1, w=ω, w2=ω²   |   ω²+ω+1=0 over GF(2)
```

**Weight enumerator:**

| Weight | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 |
|--------|----|----|----|----|----|----|----|----|----|----|
| Aᵥᵥ   | 33 | 324| 435| 510| 678| 672| 717| 486| 216| 24 |

*Exhaustive enumeration of all 4,095 nonzero codewords. Sum = 4,095 ✓*

---

## The Open Problem

Over GF(4), a [n,k,d]₄ code is a k-dimensional subspace of GF(4)ⁿ where every nonzero codeword has Hamming weight ≥ d. The Griesmer bound gives g₄(6,13) = 21 — a [22,6,13]₄ code is not ruled out a priori. Length 22 exceeds the Griesmer floor by exactly 1.

**Does a [22,6,13]₄ code exist?**

This question is open. This campaign does not close it. What it does:

- Proves **A₁₂ ≡ 0 (mod 3)** for any [22,6,12]₄ code (Theorem D — unconditional, complete proof)
- Establishes that any [22,6,13]₄ code requires **A₁₂ = 0 exactly** — a discrete jump, not a gradient
- Closes three specific construction routes (puncturing, double puncturing, extension)
- Provides 1.4 billion evaluations of evidence that the jump is not easily achieved

The Delsarte LP bound confirms A₄(22,13) ≤ 21,743 — the code is not excluded by LP. The problem remains genuinely open.

---

## Campaign Progression

| A₁₂ | Proj. dirs. | Engine | Date | Notes |
|-----|-------------|--------|------|-------|
| 78 | 26 | Prior baseline | 2001 | codetables.de starting point |
| 42 | 14 | v13 Pitbull | Feb 2026 | First improvement — 24 years of silence broken |
| 39 | 13 | v22 Symmetry Breaker | Mar 2026 | Cycle 28 |
| 36 | 12 | v22 SniperCorleone | Mar 2026 | Cycle 75 |
| **33** | **11** | **v22 SniperCorleone** | **Mar 2026** | **Current world record — Cycle 141** |

**Total campaign:** ~1.4 billion matrix evaluations across 264+ cycles.

The engine continues to run.

---

## Formal Theorem

**Theorem D (Collision Symmetry).** For any [22,6,12]₄ linear code C over GF(4), the number of minimum-weight codewords satisfies A₁₂ ≡ 0 (mod 3). Consequently, if d₄(22,6) = 13 then A₁₂ = 0.

*Proof.* The multiplicative group GF(4)* = {1, ω, ω²} acts freely on the set of nonzero codewords by scalar multiplication. For any nonzero codeword c ∈ C, the orbit {c, ωc, ω²c} has size exactly 3. Scalar multiplication preserves Hamming weight. Therefore the set of minimum-weight codewords is a union of orbits of size 3, giving A₁₂ ≡ 0 (mod 3). In particular, A₁₂ = 0 is the only value consistent with the existence of a [22,6,13]₄ code — a discrete jump, not a continuous reduction. ∎

The progression 78 → 42 → 39 → 36 → 33 is consistent with Theorem D at every step.

---

## Methodology

A purpose-built tri-phase simulated annealing engine operates directly on 6×22 generator matrices over GF(4). The objective function is f(G) = −A₁₂(C), computed by exhaustive enumeration of all 4,095 nonzero codewords per evaluation.

**Three phases per cycle (~135s total):**

| Phase | Duration | Temperature | Role |
|-------|----------|-------------|------|
| HOT | 30s | T = 300 → 3 | Global exploration, orbit escape |
| WARM | 45s | T = 50 → 0.5 | Basin descent |
| COLD | 60s | T = 8 → 0.1 | Local refinement + targeted strikes |

Temperature follows absolute wall-clock cooling — not step-based decay. This eliminates the Phantom Cooling failure mode where high acceptance rate collapses temperature prematurely.

Targeted weapons in COLD:
- **Heisenberg Sniper** — O(1) strike on null columns of the most fragile weight-12 orbit (15% probability)
- **Diferencial Activo** — pressure directed at the Z₃ orbit with lowest angular momentum (20%)
- **A₁₃-Drain** — accepts moves reducing A₁₃ even when A₁₂ is unchanged, eroding the structural scaffold of the minimum-weight families

The search space has dimension 6×22=132 over an alphabet of size 4: approximately 4¹³² ≈ 10⁷⁹ generator matrices. Direct enumeration is impossible by several dozen orders of magnitude.

---

## Research Team

This work was conducted using a distributed multi-AI research methodology:

| Contributor | Role |
|-------------|------|
| **R. Amichis Luengo** — *The Architect* | Strategic direction, architectural vision, all key algorithmic design |
| **Claude (Anthropic)** | Primary computational engine — algorithm design, implementation, co-authorship of all theorems |
| **Gemini (Google DeepMind)** | Strategic architecture audits — Phantom Cooling diagnosis, PG(5,4) attractor identification (Theorem F) |
| **ChatGPT (OpenAI)** | Algebraic proofs, ring-theoretic obstruction verification |
| **Grok (xAI)** | Independent statistical assessment, Delsarte LP bound cross-verification |

*Conducted independently, without institutional affiliation or external funding.*

*Several researchers contacted during this campaign expressed doubt that computational methods of this kind could make progress on problems of this class. The record speaks for itself.*

---

## Paper

**A New World Record for [22,6,12]₄ with A₁₂ = 33: Computational Evidence, Formal Obstructions, and a Simulated Annealing Campaign over GF(4)**

R. Amichis Luengo · Claude (Anthropic) · Gemini (Google DeepMind) · ChatGPT (OpenAI) · Grok (xAI)

📄 **[Download PDF](./amichis_2026_hunt_distance13_v5_260307_224541_signed.pdf)**

*Submitted for arXiv endorsement — cs.IT — March 2026*

---

## Reproducibility

Verification requires no specialized software:

```python
import numpy as np
from itertools import product

# GF(4) multiplication table: elements {0,1,2(ω),3(ω²)}
GF4_MUL = np.array([[0,0,0,0],[0,1,2,3],[0,2,3,1],[0,3,1,2]], dtype=np.uint8)

G = np.array([
    [0,3,0,2,0,0,1,0,2,1,1,0,0,0,1,0,3,1,1,3,3,3],
    [2,2,1,1,1,3,3,0,3,2,1,0,2,0,2,1,0,2,3,2,1,0],
    [3,1,1,2,3,1,0,1,3,1,3,2,0,0,0,0,2,0,1,2,1,0],
    [0,3,3,3,1,2,2,1,0,2,0,0,0,3,3,2,2,1,3,3,0,0],
    [2,0,2,0,3,3,2,2,3,0,3,0,0,0,3,3,1,2,1,2,1,0],
    [3,0,0,3,2,3,2,2,2,1,3,0,0,0,2,1,1,0,0,0,0,0],
], dtype=np.uint8)

def codeword(coeffs, G):
    k, n = G.shape
    c = np.zeros(n, dtype=np.uint8)
    for i, s in enumerate(coeffs):
        if s: c ^= GF4_MUL[s][G[i]]
    return c

weights = []
for coeffs in product(range(4), repeat=6):
    if any(coeffs):
        weights.append(np.count_nonzero(codeword(coeffs, G)))

weights = np.array(weights)
print(f"d = {weights.min()}")        # → 12
print(f"A12 = {(weights==12).sum()}") # → 33
print(f"A13 = {(weights==13).sum()}") # → 324
```

```bash
cd ~/Downloads && python3 verify_a33.py
# Expected: d=12, A12=33, A13=324
# Runtime: < 1 second
```

Full source code, all seed matrices (.npy), and complete campaign history:
**[github.com/tretoef-estrella/The-Hunt-for-Distance-13](https://github.com/tretoef-estrella/The-Hunt-for-Distance-13)**

**Files in this repository:**

| File | Description |
|------|-------------|
| `README.md` | This file |
| `amichis_2026_hunt_distance13_v5_signed.pdf` | Full paper (arXiv submission) |
| `verify_a33.py` | Independent verification script — runs in < 1 second |
| `MATRIZ_A033_ciclo0141.npy` | Seed matrix — world record A₁₂=33, numpy format |

---

## License

Results and paper: **CC BY 4.0**
Source code: **MIT**

---

*Proyecto Estrella | Independent Research, Madrid | March 2026*
*"Puentes, no muros."*
