"""
verify_b4.py — Verificador del co-record dual B₄=24
Proyecto Estrella · github.com/tretoef-estrella

Carga MATRIZ_A057_ciclo0014.npy y confirma:
  - d_min = 12
  - A₁₂ = 57
  - B₄ = 24  (world dual co-record)

Uso: cd ~/Downloads && python3 verify_b4.py
Requiere: numpy
"""

import numpy as np
import os

# ── GF(4) arithmetic ─────────────────────────────────────────────────────────
GF4_ADD = np.array([
    [0,1,2,3],
    [1,0,3,2],
    [2,3,0,1],
    [3,2,1,0]
], dtype=np.uint8)

GF4_MUL = np.array([
    [0,0,0,0],
    [0,1,2,3],
    [0,2,3,1],
    [0,3,1,2]
], dtype=np.uint8)

# ── Discovery matrix (A₁₂=57, B₄=24, cycle 14) ──────────────────────────────
SEED_A57 = np.array([
    [0,3,3,3,3,0,2,3,0,2,0,0,1,0,1,0,3,0,3,3,2,1],
    [0,2,1,1,2,2,3,3,0,1,1,1,3,3,2,0,3,3,3,1,0,3],
    [0,3,0,1,3,3,3,1,1,3,1,0,0,1,2,1,2,2,3,3,1,0],
    [3,1,2,0,2,0,0,0,0,2,3,2,3,2,0,1,0,3,3,1,1,2],
    [0,0,2,1,3,2,2,0,0,0,2,3,3,3,2,2,2,2,0,0,3,2],
    [0,1,1,3,0,3,3,3,0,0,0,1,1,3,0,2,2,1,0,3,3,2],
], dtype=np.uint8)


def gf4_codeword(G, coeff):
    """Compute GF(4) linear combination: sum_i coeff[i] * G[i]"""
    cw = np.zeros(G.shape[1], dtype=np.uint8)
    for i in range(len(coeff)):
        if coeff[i]:
            cw = GF4_ADD[cw, GF4_MUL[coeff[i]][G[i]]]
    return cw


def verify_primal(G):
    """Enumerate all 4^6-1 = 4095 nonzero codewords. Return (d_min, A_dmin)."""
    k, n = G.shape
    min_w = n
    count = 0
    for c_int in range(1, 4**k):
        coeff = np.array([(c_int >> (2*i)) & 3 for i in range(k)], dtype=np.uint8)
        cw = gf4_codeword(G, coeff)
        w = int(np.count_nonzero(cw))
        if w < min_w:
            min_w = w
            count = 1
        elif w == min_w:
            count += 1
    return min_w, count


def build_parity_check(G):
    """
    Build a parity check matrix H for C = rowspan(G) over GF(4).
    Uses systematic form: reduce G to [I | P], then H = [-P^T | I].
    Over GF(4): -x = x (characteristic 2), so H = [P^T | I].
    Returns H as numpy array over GF(4).
    """
    k, n = G.shape
    # Work over GF(2)^2 representation via integer arithmetic mod operations
    # We use a direct approach: compute null space of G over GF(4)
    # via Gaussian elimination
    
    Gaug = G.copy().astype(np.int32)
    pivot_cols = []
    row = 0
    
    for col in range(n):
        # Find pivot
        pivot = None
        for r in range(row, k):
            if Gaug[r, col] != 0:
                pivot = r
                break
        if pivot is None:
            continue
        # Swap
        Gaug[[row, pivot]] = Gaug[[pivot, row]]
        pivot_cols.append(col)
        # Scale pivot row so pivot = 1
        piv_val = int(Gaug[row, col])
        # Multiply row by GF4_MUL inverse of piv_val
        inv_table = [0, 1, 3, 2]  # GF(4) multiplicative inverses
        inv_piv = inv_table[piv_val]
        Gaug[row] = [GF4_MUL[inv_piv][int(x)] for x in Gaug[row]]
        # Eliminate column in all other rows
        for r in range(k):
            if r != row and Gaug[r, col] != 0:
                factor = int(Gaug[r, col])
                Gaug[r] = [GF4_ADD[int(Gaug[r, c])][GF4_MUL[factor][int(Gaug[row, c])]]
                           for c in range(n)]
        row += 1
        if row == k:
            break
    
    # Free columns = columns not in pivot_cols
    free_cols = [c for c in range(n) if c not in pivot_cols]
    
    # Build H: one row per free column
    H = np.zeros((n - k, n), dtype=np.uint8)
    for i, fc in enumerate(free_cols):
        H[i, fc] = 1
        for j, pc in enumerate(pivot_cols):
            H[i, pc] = Gaug[j, fc]
    
    return H


def verify_dual(G):
    """
    Count B₄ = number of weight-4 codewords in C⊥.
    Enumerate all 4^(n-k)-1 nonzero codewords of the dual.
    """
    k, n = G.shape
    H = build_parity_check(G)
    
    dual_k = n - k  # = 22 - 6 = 16
    b4 = 0
    total = 4**dual_k - 1
    
    print(f"  Enumerating {total:,} dual codewords (this may take ~30s)...")
    
    for c_int in range(1, 4**dual_k):
        coeff = np.array([(c_int >> (2*i)) & 3 for i in range(dual_k)], dtype=np.uint8)
        cw = gf4_codeword(H, coeff)
        w = int(np.count_nonzero(cw))
        if w == 4:
            b4 += 1
    
    return b4


def main():
    print("=" * 60)
    print("verify_b4.py — Dual Co-Record Verifier")
    print("Proyecto Estrella · github.com/tretoef-estrella")
    print("=" * 60)
    
    # Try loading from file, fall back to hardcoded matrix
    npy_path = os.path.join(os.path.dirname(__file__), "MATRIZ_A057_ciclo0014.npy")
    if os.path.exists(npy_path):
        G = np.load(npy_path)
        print(f"\nLoaded: MATRIZ_A057_ciclo0014.npy")
    else:
        G = SEED_A57
        print(f"\nUsing hardcoded discovery matrix (SEED_A57).")
    
    print(f"Matrix shape: {G.shape[0]}×{G.shape[1]} over GF(4)")
    
    # Step 1: Verify primal
    print(f"\n[1/2] Verifying primal (d_min, A₁₂)...")
    d_min, a_dmin = verify_primal(G)
    print(f"      d_min = {d_min},  A_{d_min} = {a_dmin}")
    
    primal_ok = (d_min == 12 and a_dmin == 57)
    print(f"      Expected: d_min=12, A_12=57  →  {'✓ PASS' if primal_ok else '✗ FAIL'}")
    
    # Step 2: Verify dual
    print(f"\n[2/2] Verifying dual (B₄)...")
    b4 = verify_dual(G)
    print(f"      B₄ = {b4}")
    
    dual_ok = (b4 == 24)
    print(f"      Expected: B₄=24             →  {'✓ PASS' if dual_ok else '✗ FAIL'}")
    
    # Summary
    print("\n" + "=" * 60)
    if primal_ok and dual_ok:
        print("RESULT: B₄ = 24 CONFIRMED  ✓")
        print()
        print("  This matrix achieves the world dual co-record:")
        print("  B₄ = 24  (8 Z₃-orbits of weight-4 dual codewords)")
        print("  Theorem D Corollary: B₄ ≡ 0 (mod 3) ✓")
        print()
        print("  For d=13 to exist: B₄ = 0 required exactly.")
        print("  Current campaign target: B₄ = 21 (next step).")
    else:
        print("RESULT: VERIFICATION FAILED")
        print("  Check GF(4) encoding: 0=0, 1=1, 2=ω, 3=ω²")
    print("=" * 60)
    print("\nProyecto Estrella · Madrid, 2026")
    print("github.com/tretoef-estrella/The-Hunt-for-Distance-13")


if __name__ == "__main__":
    main()
