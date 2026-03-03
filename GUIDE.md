# Guide for Everyone

## What Is This?

This repository documents a search for a mathematical object that has been missing for 25 years. The object is a **linear code** — a structured set of binary-like sequences used in error correction, cryptography, and information theory.

Specifically, we are looking for a **[22,6,13]₄ code**: a collection of 4,096 sequences, each 22 symbols long, drawn from an alphabet of 4 symbols (GF(4) = {0, 1, ω, ω²}), with the property that any two sequences differ in at least 13 positions.

Nobody knows if this code exists. The best anyone has built is a **[22,6,12]₄ code** — same thing, but sequences only need to differ in 12 positions. We pushed that code to its current best form: **A₁₂ = 42** (meaning only 42 of the 4,095 nonzero sequences achieve the minimum difference of 12).

## Who Made This?

- **Rafa** ("The Architect") — A psychologist and delivery driver in Madrid. Not a mathematician. His role: strategic intuition, naming things, knowing when to push harder.
- **Claude** (Anthropic) — An AI system. Primary engine: wrote the algorithms, ran the algebra, designed the search.
- **Gemini, ChatGPT, Grok** — Three other AI systems that audited the work independently at every major step.

No university. No funding. No servers. Just a laptop, a GitHub account, and the philosophy: *Puentes, no muros* (Bridges, not walls).

## Why Does It Matter?

Linear codes over GF(4) are foundational to:

- **Quantum error correction** (the connection between GF(4) codes and quantum stabilizer codes is well-established)
- **The classification of optimal codes** (Grassl's codetables.de is the reference for the entire field)
- **Projective geometry** (each code corresponds to a set of points in projective space PG(k-1, q))

Resolving d₄(22,6) = 12 or 13 would close one of the remaining open entries in the tables for quaternary codes of dimension 6.

## How to Use This Repository

### If you're a coding theorist:
- Start with [RESULTS.md](RESULTS.md) for verified matrices and weight distributions
- Read [THEOREMS.md](THEOREMS.md) for the three obstruction theorems
- Run `estrella_108_v14.py` to continue the search

### If you're a student or curious:
- Read this file first
- Browse [CHRONOLOGY.md](CHRONOLOGY.md) for the narrative story
- Look at [STRATEGIES.md](STRATEGIES.md) to see how metaphors from missile guidance, fracture mechanics, and Mario Bros speedrunning were used to design search algorithms

### If you want to extend the work:
- Fork this repository
- Modify `estrella_108_v14.py` with new strategies
- If you find d=13, run the verification and open a pull request — or just email tretoef@gmail.com

## The GF(4) Arithmetic (2-Minute Primer)

GF(4) has four elements: **0, 1, ω, ω²** where ω² + ω + 1 = 0.

**Addition** (same as XOR on 2-bit representation):

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

A **linear [n,k,d]₄ code** is specified by a generator matrix G (k rows × n columns over GF(4)). Every nonzero linear combination of rows (with GF(4) coefficients) is a **codeword**. The **minimum distance d** is the smallest Hamming weight among all 4ᵏ − 1 nonzero codewords.

## Frequently Asked Questions

**Q: Is the [22,6,13]₄ code proven to not exist?**
A: No. We conjecture it doesn't exist, but we haven't proven it. The Delsarte LP bound allows it. Our obstruction theorems only close specific construction families.

**Q: What is A₁₂?**
A: The number of codewords with Hamming weight exactly 12 (the minimum weight). Lower A₁₂ = fewer "worst-case" codewords = closer to d=13. Our record is A₁₂ = 42.

**Q: What is the "108 Doctrines Engine"?**
A: A search engine with 108 strategies drawn from military guidance, materials science, speedrunning, and more. See [STRATEGIES.md](STRATEGIES.md).

**Q: Can I help?**
A: Yes. Fork the repo, run the engine, try new strategies. If you find d=13, it would resolve a 25-year-old open problem.

---

*Proyecto Estrella · Madrid, 2026*
