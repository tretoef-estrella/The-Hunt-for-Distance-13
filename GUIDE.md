# Guide for Everyone

## What Is This?

This repository documents a search for a mathematical object that has been missing for 25 years. The object is a **linear code** — a structured set of sequences used in error correction, cryptography, and information theory.

Specifically, we are looking for a **[22,6,13]₄ code**: a collection of 4,096 sequences, each 22 symbols long, drawn from an alphabet of 4 symbols (GF(4) = {0, 1, ω, ω²}), with the property that any two sequences differ in at least 13 positions.

Nobody knows if this code exists. The best known construction achieves **d = 12**. The current world records are **A₁₂ = 33** (primal) and **B₄ = 24** (dual co-record) — March 2026.

---

## Who Made This?

- **Rafael Amichis Luengo** ("The Architect") — Independent researcher, Madrid. Strategy, direction, architecture.
- **Claude** (Anthropic) — Primary computational engine. Algorithm design, algebraic analysis, code construction.
- **Gemini** (Google) · **ChatGPT** (OpenAI) · **Grok** (xAI) — Independent adversarial auditors at every major step.

No university. No funding. No servers. Just a laptop, a GitHub account, and the philosophy: *Puentes, no muros* (Bridges, not walls).

---

## Why Does It Matter?

Linear codes over GF(4) are foundational to quantum error correction, coding theory classification, and projective geometry over finite fields. Resolving d₄(22,6) = 12 or 13 would close one of the remaining open entries in the tables for quaternary codes of dimension 6 — a problem open since Grassl (2001).

---

## The GF(4) Arithmetic (2-Minute Primer)

GF(4) has four elements: **0, 1, ω, ω²** where ω² + ω + 1 = 0 over GF(2).

**Addition** (bitwise XOR on 2-bit representation):

| + | 0 | 1 | ω | ω² |
|---|---|---|---|---|
| 0 | 0 | 1 | ω | ω² |
| 1 | 1 | 0 | ω² | ω |
| ω | ω | ω² | 0 | 1 |
| ω² | ω² | ω | 1 | 0 |

**Multiplication:**

| × | 0 | 1 | ω | ω² |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| 1 | 0 | 1 | ω | ω² |
| ω | 0 | ω | ω² | 1 |
| ω² | 0 | ω² | 1 | ω |

A **linear [n,k,d]₄ code** is specified by a generator matrix G (k rows × n columns over GF(4)). Every nonzero GF(4)-linear combination of rows is a **codeword**. The **minimum distance d** is the smallest Hamming weight among all 4ᵏ − 1 nonzero codewords. **Encoding:** 0=0, 1=1, 2=ω, 3=ω².

---

## Repository Contents

| File | Description |
|------|-------------|
| README.md | Project overview and world record matrix |
| GUIDE.md | This file |
| RESULTS.md | All verified matrices, weight enumerators, campaign data |
| THEOREMS.md | Six obstruction theorems + five structural theorems with proofs |
| DUAL_ATTACK.md | The dual-spectrum B₄ attack and co-record B₄=24 |
| CHRONOLOGY.md | Narrative timeline of the full campaign |
| OPEN_PROBLEMS.md | What remains open and how to contribute |
| CITATION.md | Citation metadata (BibTeX, APA, IEEE) |
| LICENSE.md | Business Source License 1.1 + SAMAEL Decree |
| MATRIZ_A033_ciclo0141.npy | World record matrix A₁₂=33 |
| MATRIZ_A057_ciclo0014.npy | Dual co-record matrix B₄=24 |
| MATRIZ_A036_ciclo0075.npy | Intermediate record A₁₂=36 |
| MATRIZ_A039_ciclo0001.npy | Intermediate record A₁₂=39 |
| verify_a33.py | Standalone verifier — confirms A₁₂=33 in <1s |
| amichis_2026_hunt_distance13_v7.pdf | Preprint (March 2026) |

---

## Frequently Asked Questions

**Q: Is [22,6,13]₄ proven not to exist?**  
A: No. We conjecture it doesn't exist, but we have not proved it. Our obstruction theorems close specific construction families, not all possibilities.

**Q: What is A₁₂?**  
A: The number of codewords with Hamming weight exactly 12 (the minimum). Lower A₁₂ = structurally closer to d=13. Current record: A₁₂ = 33.

**Q: What is B₄?**  
A: The number of weight-4 codewords in the dual code C⊥. Each corresponds to a cluster of 4 dependent columns in G — a structural obstacle to d=13. By Theorem D Corollary, B₄ ≡ 0 (mod 3). Current co-record: B₄ = 24.

**Q: Why do both A₁₂ and B₄ change by multiples of 3?**  
A: Theorem D and its Corollary. The GF(4)* scalar action groups both primal and dual codewords into orbits of size 3.

**Q: What is the Heisenberg Constant?**  
A: E[w] = 67584/4095 = 16.504029... — the exact mean codeword weight any [22,6,13]₄ code must satisfy (MacWilliams identities, B₁ = 0).

**Q: Where is the search methodology?**  
A: The search methodology is documented separately and will be made available upon request after arXiv publication.

---

## The Conjecture

> **Conjecture.** d₄(22,6) = 12. No [22,6,13]₄ linear code exists.

Supported by: 1.5B+ evaluations · 30+ closed construction routes · 6 obstruction theorems · dual co-record B₄=24.

---

*"Puentes, no muros. Es una orden conseguirlo."*

**Proyecto Estrella · Madrid, 2026 · tretoef@gmail.com**
