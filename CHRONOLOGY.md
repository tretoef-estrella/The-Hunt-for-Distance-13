# Chronology of the Hunt

*A timeline of the campaign to resolve d₄(22,6) = 12 or 13.*

---

## Origins: AEGIS Crystal Labyrinth (January–February 2026)

The [22,6,d]₄ problem was not the original target. It emerged as a byproduct.

The AEGIS Crystal Labyrinth — a post-quantum cryptographic defense system built on PG(11,4) and the Knuth Type II semifield over GF(4) — required evaluation codes of maximum distance. SAMAEL (Beast 10), the system's final judgment layer, attempted construction via fusion-column codes. The best achievable: d = 11. SAMAEL's verdict was clear: if [22,6,13]₄ exists, it does not arise from presemifield evaluation codes. A new campaign was needed.

---

## Phase 1: First Contact (February 2026)

The GF(4) arithmetic engines from AEGIS became the foundation of Error Code Lab. First baseline: d = 12, A₁₂ = 78 (26 projective directions).

The first structural theorem was identified: **A₁₂ ≡ 0 (mod 3)** (Theorem D). The scalar action of GF(4)* groups minimum-weight codewords into orbits of size 3. The sequence of possible records was fixed: 78, 75, ... 33, 30, ... 0.

---

## Phase 2: Obstruction Theorems (February 2026)

Three fundamental obstruction theorems were proven:

**Theorem A** — Puncturing from [23,6,13]₄ is impossible.  
**Theorem B** — Double puncturing from [24,7,13]₄ yields d ≤ 11 for all 276 pairs.  
**Theorem C** — Extension from [21,5,13]₄ is structurally irreducible.

These theorems closed the most natural construction families.

---

## Phase 3: The A₁₂ Records (February–March 2026)

| Date | Record | Method |
|------|--------|--------|
| Feb 2026 | A₁₂ = 60 | Exhaustive sixth-row search |
| Feb 2026 | A₁₂ = 51 | Gradient descent |
| Feb 2026 | A₁₂ = 48 | Gradient descent |
| Feb 2026 | **A₁₂ = 42** ★ | Pitbull row-recombination |
| Feb 2026 | A₁₂ = 42 (floor confirmed) | Italian Job — 720M evaluations, 7.5 hours |
| Mar 2026 | **A₁₂ = 39** ★ | Symmetry-breaking campaign |
| Mar 2026 | **A₁₂ = 36** ★ | Cascade descent |
| Mar 2026 | **A₁₂ = 33** ★ | World record — confirmed twice |

**Previous world record: A₁₂ = 42 (Grassl, 2001) — stood 25 years.**

The Italian Job (v14/v15) confirmed A₁₂ = 42 is a geometric floor, not a local accident. ~720M evaluations over 7.5 hours with no improvement. This led to Theorem F (PG(5,4) Attractor). Escaping required the Symmetry Breaker: HOT phase valley crossing with d=11 access.

---

## Phase 4: Structural Consolidation (March 2026)

With A₁₂ = 33 established, 293+ additional cycles confirmed it as a structural attractor. The AZRAEL engine (orbit atlas + surgical fixes) ran continuously, tracking every Z₃ orbit of minimum-weight codewords. A₁₃ drain reduced the weight-13 population from 327 to approximately 95 — a 71% erosion — without breaking A₁₂ = 33.

Theorem E (CSP Collapse) and Theorem F (PG(5,4) Attractor/Asymmetry) were proven. 30+ construction routes closed. Total evaluations crossed 1.5 billion.

---

## Phase 5: Dual-Spectrum Attack (March 2026)

With A₁₂ = 33 resistant to further direct improvement, a second front was opened: the **dual-spectrum attack**, targeting B₄ — the number of weight-4 codewords in the dual code C⊥.

**Theorem D Corollary (Dual Symmetry):** B₄ ≡ 0 (mod 3). Consequence: any [22,6,13]₄ code requires B₄ = 0 exactly.

The dual cascade:

| Step | B₄ | Z₃-orbits | Status |
|------|----|-----------|--------|
| Baseline | 36 | 12 | at A₁₂=33 |
| Step 1 | 33 | 11 | confirmed |
| Step 2 | 30 | 10 | confirmed |
| **Step 3** | **24** | **8** | **world co-record — cycle 14** |
| Next target | 21 | 7 | active |

**B₄ = 24 confirmed reproducibly.** Discovery matrix: `MATRIZ_A057_ciclo0014.npy`.

Every step divisible by 3 — Theorem D Corollary confirmed at every stage.

---

## Current Status (March 2026)

- **A₁₂ = 33** — world record (11 projective directions)
- **B₄ = 24** — world dual co-record (8 Z₃ dual orbits)
- **1.5B+ evaluations** · **350+ cycles** · **30+ routes closed**
- **Active campaign:** dual descent targeting B₄ = 21

The diamond has not been found. The hunt continues on two fronts.

---

*"Puentes, no muros. Es una orden conseguirlo."*

**Proyecto Estrella · Madrid, 2026 · tretoef@gmail.com**
