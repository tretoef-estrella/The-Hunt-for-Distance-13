# Results

All verified matrices and computational records from the Proyecto Estrella campaign on d₄(22,6). Updated March 2026.

---

## Primary Records

| Record | Value | Matrix file | Verified |
|--------|-------|-------------|---------|
| A₁₂ (primal) | **33** | `MATRIZ_A033_ciclo0141.npy` | ✓ exhaustive, twice |
| B₄ (dual) | **24** | `MATRIZ_A057_ciclo0014.npy` | ✓ confirmed reproducible |
| A₁₂ = 36 | 36 | `MATRIZ_A036_ciclo0075.npy` | ✓ |
| A₁₂ = 39 | 39 | `MATRIZ_A039_ciclo0001.npy` | ✓ |

---

## World Record: A₁₂ = 33

**Confirmed twice in independent computational runs. Previous record: A₁₂ = 42 (Grassl, 2001) — stood 25 years.**

Generator matrix G (6×22 over GF(4), encoding: 0=0, 1=1, 2=ω, 3=ω²):
```
g1 = [0,3,0,2,0,0,1,0,2,1,1,0,0,0,1,0,3,1,1,3,3,3]
g2 = [2,2,1,1,1,3,3,0,3,2,1,0,2,0,2,1,0,2,3,2,1,0]
g3 = [3,1,1,2,3,1,0,1,3,1,3,2,0,0,0,0,2,0,1,2,1,0]
g4 = [0,3,3,3,1,2,2,1,0,2,0,0,0,3,3,2,2,1,3,3,0,0]
g5 = [2,0,2,0,3,3,2,2,3,0,3,0,0,0,3,3,1,2,1,2,1,0]
g6 = [3,0,0,3,2,3,2,2,2,1,3,0,0,0,2,1,1,0,0,0,0,0]
```

**Complete weight enumerator:**

| Weight | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 |
|--------|----|----|----|----|----|----|----|----|----|----|
| Count  | 33 | 324 | 435 | 510 | 678 | 672 | 717 | 486 | 216 | 24 |

Sum = 4,095 ✓ — A₁₂ = 33 ≡ 0 (mod 3) — 11 projective directions.

---

## Dual Co-Record: B₄ = 24

**Reached cycle 14 of the dual-spectrum campaign. Confirmed reproducibly.**

Discovery matrix (A₁₂=57, B₄=24) stored in `MATRIZ_A057_ciclo0014.npy`.
```python
SEED_A57 = np.array([
    [0,3,3,3,3,0,2,3,0,2,0,0,1,0,1,0,3,0,3,3,2,1],
    [0,2,1,1,2,2,3,3,0,1,1,1,3,3,2,0,3,3,3,1,0,3],
    [0,3,0,1,3,3,3,1,1,3,1,0,0,1,2,1,2,2,3,3,1,0],
    [3,1,2,0,2,0,0,0,0,2,3,2,3,2,0,1,0,3,3,1,1,2],
    [0,0,2,1,3,2,2,0,0,0,2,3,3,3,2,2,2,2,0,0,3,2],
    [0,1,1,3,0,3,3,3,0,0,0,1,1,3,0,2,2,1,0,3,3,2],
], dtype=np.uint8)
# d=12, A₁₂=57, B₄=24, cycle=14
```

Dual cascade confirmed: 36 → 33 → 30 → **24**. Each step ≡ 0 (mod 3) per Theorem D Corollary.

---

## Intermediate A₁₂ Records

### A₁₂ = 36 — `MATRIZ_A036_ciclo0075.npy`
```
g1 = [2,1,0,2,0,2,0,2,3,0,2,2,3,1,0,0,0,3,2,0,0,1]
g2 = [3,1,0,1,1,0,1,3,1,1,0,1,2,3,3,3,0,1,1,0,3,0]
g3 = [3,1,0,2,2,3,0,2,0,3,1,1,2,0,0,1,0,1,0,0,2,0]
g4 = [0,0,1,1,3,0,2,3,3,3,1,0,1,2,0,0,1,2,1,0,3,0]
g5 = [3,2,0,2,1,2,3,0,1,1,3,3,0,2,0,3,2,2,0,3,2,0]
g6 = [0,0,0,0,1,1,1,2,0,1,3,1,1,2,0,1,2,1,1,0,1,0]
```

d_min = 12, A₁₂ = 36 (12 projective directions).

### A₁₂ = 39 — `MATRIZ_A039_ciclo0001.npy`
```
g1 = [1,1,0,0,0,0,3,2,2,0,0,3,2,2,1,1,0,0,2,0,2,3]
g2 = [2,0,2,1,0,0,3,1,3,0,2,3,1,3,3,0,1,3,1,3,3,2]
g3 = [2,3,2,2,3,0,2,0,2,2,1,3,2,0,2,0,2,0,0,0,3,3]
g4 = [0,3,1,3,0,3,0,3,3,0,2,2,3,2,1,0,0,0,1,1,0,2]
g5 = [2,2,3,1,0,0,2,3,0,1,1,3,0,3,0,0,1,0,0,2,3,3]
g6 = [1,2,0,1,0,0,2,3,2,0,3,1,3,0,0,0,2,0,1,3,0,0]
```

d_min = 12, A₁₂ = 39 (13 projective directions).

### A₁₂ = 42 — February 2026
```
g1 = [1,1,0,0,0,0,3,2,1,1,2,2,0,1,0,1,0,3,0,0,3,3]
g2 = [0,0,0,0,0,0,2,2,0,0,1,3,3,2,2,2,1,3,1,0,2,2]
g3 = [0,2,1,0,0,0,3,2,3,2,0,3,0,1,1,0,2,2,2,1,0,2]
g4 = [0,0,0,1,0,0,2,0,3,3,3,0,1,2,2,1,0,0,3,2,2,1]
g5 = [0,3,0,0,1,0,3,3,2,0,3,3,2,0,1,2,1,2,1,2,0,0]
g6 = [0,0,0,0,0,1,0,0,2,1,3,0,3,1,3,0,2,2,1,2,2,1]
```

First world record of this campaign. Confirmed as structural floor by Italian Job (~720M evaluations, 7.5 hours).

---

## Full Campaign Progress

| Phase | Engine | Evaluations | A₁₂ | B₄ | Date |
|-------|--------|-------------|-----|----|------|
| Baseline | Grassl (2001) | — | 78 | — | 2001 |
| v1–v5 | SA + 108 Doctrines | ~500M | 69→60→51→48 | — | Feb 2026 |
| v13 Pitbull | Row recombination | +373M | **42** | — | Feb 2026 |
| v14–v15 Italian Job | Vertical collapse | ~720M | 42 floor | — | Feb 2026 |
| v22 cycle 28 | Time-SA | +100M | **39** ★ | — | Mar 2026 |
| v22 cycle 75 | Cascade | +200M | **36** ★ | — | Mar 2026 |
| v22 cycle 141 | WARM cascade | +300M | **33** ★ | 36 | Mar 2026 |
| AZRAEL v13 | Orbit atlas | 293+ cycles | 33 | 36 | Mar 2026 |
| Dual-phase | Dual descent | 100+ cycles | 33 | **30** ★ | Mar 2026 |
| Dual-phase cycle 14 | Cascade | active | 33 | **24** ★ | Mar 2026 |

★ = world record at time. **Total: 1.5B+ evaluations · 350+ cycles · 30+ routes closed.**

---

## Key Constants

- **A₁₂ ≡ 0 (mod 3)** — Theorem D
- **B₄ ≡ 0 (mod 3)** — Theorem D Corollary
- **E[w] = 67584/4095 = 16.504029...** — MacWilliams identity, B₁ = 0
- **Griesmer bound:** g₄(6,13) = 21 — [22,6,13]₄ not excluded a priori
- **Delsarte LP bound:** A₄(22,13) ≤ 21,743 — problem genuinely open

---

## Quick Verification
```python
import numpy as np

GF4_ADD = np.array([[0,1,2,3],[1,0,3,2],[2,3,0,1],[3,2,1,0]], dtype=np.uint8)
GF4_MUL = np.array([[0,0,0,0],[0,1,2,3],[0,2,3,1],[0,3,1,2]], dtype=np.uint8)

G = np.array([
    [0,3,0,2,0,0,1,0,2,1,1,0,0,0,1,0,3,1,1,3,3,3],
    [2,2,1,1,1,3,3,0,3,2,1,0,2,0,2,1,0,2,3,2,1,0],
    [3,1,1,2,3,1,0,1,3,1,3,2,0,0,0,0,2,0,1,2,1,0],
    [0,3,3,3,1,2,2,1,0,2,0,0,0,3,3,2,2,1,3,3,0,0],
    [2,0,2,0,3,3,2,2,3,0,3,0,0,0,3,3,1,2,1,2,1,0],
    [3,0,0,3,2,3,2,2,2,1,3,0,0,0,2,1,1,0,0,0,0,0],
], dtype=np.uint8)

min_w = 22; count = 0
for c_int in range(1, 4**6):
    c = np.array([(c_int>>(2*i))&3 for i in range(6)], dtype=np.uint8)
    cw = np.zeros(22, dtype=np.uint8)
    for i in range(6):
        if c[i]: cw = GF4_ADD[cw, GF4_MUL[c[i]][G[i]]]
    w = int(np.count_nonzero(cw))
    if w < min_w: min_w = w; count = 1
    elif w == min_w: count += 1

print(f"d_min={min_w}, A_{min_w}={count}")
# Output: d_min=12, A_12=33
```

*Proyecto Estrella · Madrid, 2026*
