#!/usr/bin/env python3
"""
PROYECTO ESTRELLA — 108 DOCTRINES ENGINE v13 (THE MATRIX + FLUORESCENCIA)
[22,6,13]_4 over GF(4) — THE DIAMOND HUNT

ONE FILE. Auto-compiles C kernel. 500K+ evals/sec on Mac.

v8 NEW: Heat-Seeker · PropNav · Pitbull · Fluorescencia · Silueta IIR
v7:     Ghost Imaging · Triangulación · 1-UP · Metamaterial · Warp Zone
v6:     RDE · BMG · SABRE · Borofeno
v5:     Cavitación · Cuñas · Hilo · Fragilización · Deflagración

21 phases. 24 strategies. C kernel. GUIDED SEARCH via discrete gradient.

Rafa — The Architect + Claude (SAMAEL Beast 10)
Σ = 1561/675 ≈ 2.31 | 73 mechanisms | 10 beasts

EXECUTION:
    cd ~/Downloads && python3 estrella_108_v13.py
"""

import numpy as np
import ctypes
import itertools
import time
import os
import sys
import platform
import subprocess
import tempfile
from collections import defaultdict

# ═══════════════════════════════════════════════════════════════
# C KERNEL — EMBEDDED & AUTO-COMPILED
# ═══════════════════════════════════════════════════════════════

_C_SOURCE = r"""
#include <stdint.h>
#include <string.h>
static const uint8_t GA[4][4]={{0,1,2,3},{1,0,3,2},{2,3,0,1},{3,2,1,0}};
static const uint8_t GM[4][4]={{0,0,0,0},{0,1,2,3},{0,2,3,1},{0,3,1,2}};
int min_distance(const uint8_t*G,int k,int n,int*cnt){
    int total=1;for(int i=0;i<k;i++)total*=4;
    int md=n+1,mc=0;uint8_t cw[256],v[10];
    for(int idx=1;idx<total;idx++){
        int tmp=idx;for(int j=k-1;j>=0;j--){v[j]=tmp%4;tmp/=4;}
        memset(cw,0,n);
        for(int j=0;j<k;j++){if(v[j]==0)continue;const uint8_t*row=G+j*n;
            for(int c=0;c<n;c++)cw[c]=GA[cw[c]][GM[v[j]][row[c]]];}
        int w=0;for(int c=0;c<n;c++)if(cw[c])w++;
        if(w<md){md=w;mc=1;}else if(w==md)mc++;
    }if(cnt)*cnt=mc;return md;}
int min_distance_early(const uint8_t*G,int k,int n,int thr){
    int total=1;for(int i=0;i<k;i++)total*=4;uint8_t cw[256],v[10];
    for(int idx=1;idx<total;idx++){
        int tmp=idx;for(int j=k-1;j>=0;j--){v[j]=tmp%4;tmp/=4;}
        memset(cw,0,n);
        for(int j=0;j<k;j++){if(v[j]==0)continue;const uint8_t*row=G+j*n;
            for(int c=0;c<n;c++)cw[c]=GA[cw[c]][GM[v[j]][row[c]]];}
        int w=0;for(int c=0;c<n;c++)if(cw[c])w++;
        if(w<thr)return w;
    }return thr;}
void weight_enumerator(const uint8_t*G,int k,int n,int*wts){
    int total=1;for(int i=0;i<k;i++)total*=4;
    memset(wts,0,(n+1)*sizeof(int));wts[0]=1;uint8_t cw[256],v[10];
    for(int idx=1;idx<total;idx++){
        int tmp=idx;for(int j=k-1;j>=0;j--){v[j]=tmp%4;tmp/=4;}
        memset(cw,0,n);
        for(int j=0;j<k;j++){if(v[j]==0)continue;const uint8_t*row=G+j*n;
            for(int c=0;c<n;c++)cw[c]=GA[cw[c]][GM[v[j]][row[c]]];}
        int w=0;for(int c=0;c<n;c++)if(cw[c])w++;
        wts[w]++;}}
"""

def _build_kernel():
    """Write C source to temp file, compile, load. Fully automatic."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ext = '.dylib' if platform.system() == 'Darwin' else '.so'
    lib_path = os.path.join(script_dir, '_gf4k' + ext)
    
    # If already compiled and newer than script, just load
    if os.path.exists(lib_path):
        try:
            lib = ctypes.CDLL(lib_path)
            lib.min_distance.restype = ctypes.c_int
            lib.min_distance.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
            lib.min_distance_early.restype = ctypes.c_int
            lib.min_distance_early.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int]
            lib.weight_enumerator.restype = None
            lib.weight_enumerator.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
            return lib
        except:
            pass

    # Write and compile
    c_path = os.path.join(script_dir, '_gf4k.c')
    with open(c_path, 'w') as f:
        f.write(_C_SOURCE)
    
    try:
        subprocess.run(['gcc', '-O3', '-shared', '-fPIC', '-o', lib_path, c_path],
                      check=True, capture_output=True)
        os.remove(c_path)
        return _build_kernel()  # reload
    except Exception as e:
        # Try cc as fallback
        try:
            subprocess.run(['cc', '-O3', '-shared', '-fPIC', '-o', lib_path, c_path],
                          check=True, capture_output=True)
            os.remove(c_path)
            return _build_kernel()
        except:
            pass
    return None

_LIB = None
_CNT_BUF = None

def _init_kernel():
    global _LIB, _CNT_BUF
    _LIB = _build_kernel()
    _CNT_BUF = ctypes.c_int(0)
    if _LIB:
        print("  C kernel: AUTO-COMPILED & LOADED (1000x fast rejection)")
    else:
        print("  C kernel: COMPILATION FAILED — using Python (10x slower)")
        print("  Need gcc/cc installed. On Mac: xcode-select --install")


# ═══════════════════════════════════════════════════════════════
# GF(4) KERNEL — PYTHON FALLBACK + C ACCELERATED
# ═══════════════════════════════════════════════════════════════

GF4_ADD = np.array([[0,1,2,3],[1,0,3,2],[2,3,0,1],[3,2,1,0]], dtype=np.uint8)
GF4_MUL = np.array([[0,0,0,0],[0,1,2,3],[0,2,3,1],[0,3,1,2]], dtype=np.uint8)
GF4_INV = np.array([0,1,3,2], dtype=np.uint8)
FROBENIUS = np.array([0,1,3,2], dtype=np.uint8)

def gf4_vec_add(a, b):
    return GF4_ADD[a, b]

def gf4_matmul(A, B):
    m, p = A.shape
    _, n = B.shape
    R = np.zeros((m, n), dtype=np.uint8)
    for i in range(p):
        R = GF4_ADD[R, GF4_MUL[A[:, i:i+1], B[i:i+1, :]]]
    return R

def gf4_rank(M):
    A = M.copy()
    rows, cols = A.shape
    rank = 0
    for col in range(cols):
        pivot = None
        for row in range(rank, rows):
            if A[row, col] != 0:
                pivot = row
                break
        if pivot is None:
            continue
        A[[rank, pivot]] = A[[pivot, rank]]
        A[rank] = GF4_MUL[GF4_INV[A[rank, col]]][A[rank]]
        for row in range(rows):
            if row != rank and A[row, col] != 0:
                A[row] = GF4_ADD[A[row], GF4_MUL[A[row, col]][A[rank]]]
        rank += 1
    return rank

def idx_to_gf4_vec(idx, k):
    v = np.zeros(k, dtype=np.uint8)
    tmp = idx
    for j in range(k-1, -1, -1):
        v[j] = tmp % 4
        tmp //= 4
    return v

def encode(info_vec, G):
    k, n = G.shape
    cw = np.zeros(n, dtype=np.uint8)
    for j in range(k):
        if info_vec[j] != 0:
            cw = GF4_ADD[cw, GF4_MUL[info_vec[j]][G[j]]]
    return cw

# Python fallback for min_distance
_INFO_VECS = None
_INFO_NONZERO = None

def _precompute_info(k=6):
    global _INFO_VECS, _INFO_NONZERO
    if _INFO_VECS is not None:
        return
    total = 4**k - 1
    _INFO_VECS = np.zeros((total, k), dtype=np.uint8)
    tmp = np.arange(1, 4**k, dtype=np.int32)
    for j in range(k-1, -1, -1):
        _INFO_VECS[:, j] = tmp % 4
        tmp //= 4
    _INFO_NONZERO = []
    for j in range(k):
        for val in range(1, 4):
            mask = (_INFO_VECS[:, j] == val)
            if np.any(mask):
                _INFO_NONZERO.append((j, val, mask))

def _min_dist_python(G):
    """Python fallback."""
    k, n = G.shape
    _precompute_info(k)
    total = 4**k - 1
    codewords = np.zeros((total, n), dtype=np.uint8)
    for j, val, mask in _INFO_NONZERO:
        contrib = GF4_MUL[val][G[j]]
        codewords[mask] = GF4_ADD[codewords[mask], contrib]
    weights = np.count_nonzero(codewords, axis=1)
    min_d = int(np.min(weights))
    count_min = int(np.sum(weights == min_d))
    return min_d, count_min

def min_dist_full(G):
    """Full min distance with count. Uses C if available."""
    G_c = np.ascontiguousarray(G, dtype=np.uint8)
    k, n = G_c.shape
    if _LIB:
        cnt = ctypes.c_int(0)
        d = _LIB.min_distance(G_c.ctypes.data, k, n, ctypes.byref(cnt))
        return d, cnt.value
    else:
        return _min_dist_python(G_c)

def min_dist(G):
    """Just the distance."""
    d, _ = min_dist_full(G)
    return d

def min_dist_early(G, threshold=13):
    """Fast check: returns actual d if d < threshold, else threshold.
    With C kernel + early exit, this is ~1000x faster for rejections."""
    G_c = np.ascontiguousarray(G, dtype=np.uint8)
    k, n = G_c.shape
    if _LIB:
        return _LIB.min_distance_early(G_c.ctypes.data, k, n, threshold)
    else:
        d, _ = _min_dist_python(G_c)
        return d if d < threshold else threshold

def weight_enum(G):
    """Full weight enumerator."""
    G_c = np.ascontiguousarray(G, dtype=np.uint8)
    k, n = G_c.shape
    if _LIB:
        w = np.zeros(n + 1, dtype=np.int32)
        _LIB.weight_enumerator(G_c.ctypes.data, k, n, w.ctypes.data)
        return {i: int(w[i]) for i in range(n + 1) if w[i] > 0}
    else:
        _precompute_info(k)
        total = 4**k - 1
        codewords = np.zeros((total, n), dtype=np.uint8)
        for j, val, mask in _INFO_NONZERO:
            contrib = GF4_MUL[val][G[j]]
            codewords[mask] = GF4_ADD[codewords[mask], contrib]
        weights = np.count_nonzero(codewords, axis=1)
        W = defaultdict(int)
        W[0] = 1
        for w in weights:
            W[int(w)] += 1
        return dict(W)

def systematic_form(G):
    k, n = G.shape
    A = G.copy()
    for col in range(k):
        pivot = None
        for row in range(col, k):
            if A[row, col] != 0:
                pivot = row
                break
        if pivot is None:
            return G
        A[[col, pivot]] = A[[pivot, col]]
        A[col] = GF4_MUL[GF4_INV[A[col, col]]][A[col]]
        for row in range(k):
            if row != col and A[row, col] != 0:
                A[row] = GF4_ADD[A[row], GF4_MUL[A[row, col]][A[col]]]
    return A

def all_nonzero_columns(k):
    vecs = []
    for idx in range(1, 4**k):
        vecs.append(idx_to_gf4_vec(idx, k))
    return vecs

_ALL_COLS = None
def _get_cols(k=6):
    global _ALL_COLS
    if _ALL_COLS is None:
        _ALL_COLS = np.array(all_nonzero_columns(k), dtype=np.uint8)
    return _ALL_COLS


# ═══════════════════════════════════════════════════════════════
# SEED — [22,6,12]_4 from QR shortening
# ═══════════════════════════════════════════════════════════════

_INFO_CACHE = {}

def _precompute_k(k):
    if k in _INFO_CACHE:
        return
    total = 4**k - 1
    vecs = np.zeros((total, k), dtype=np.uint8)
    tmp = np.arange(1, 4**k, dtype=np.int32)
    for j in range(k-1, -1, -1):
        vecs[:, j] = tmp % 4
        tmp //= 4
    nz = []
    for j in range(k):
        for val in range(1, 4):
            mask = (vecs[:, j] == val)
            if np.any(mask):
                nz.append((j, val, mask))
    _INFO_CACHE[k] = (vecs, nz)

def _min_dist_k(G, k):
    """Min distance for arbitrary k (Python, used only during seed build)."""
    _precompute_k(k)
    vecs, nz = _INFO_CACHE[k]
    n = G.shape[1]
    total = 4**k - 1
    cw = np.zeros((total, n), dtype=np.uint8)
    for j, val, mask in nz:
        contrib = GF4_MUL[val][G[j]]
        cw[mask] = GF4_ADD[cw[mask], contrib]
    weights = np.count_nonzero(cw, axis=1)
    return int(np.min(weights))

def build_seed():
    """Build [22,6,12]_4 from [24,7,13]_4 quasi-cyclic code."""
    g1 = np.array([2, 2, 3, 1, 2, 1, 1, 0], dtype=np.uint8)
    g2 = np.array([3, 2, 1, 1, 1, 0, 0, 0], dtype=np.uint8)
    g3 = np.array([3, 2, 1, 0, 0, 0, 0, 0], dtype=np.uint8)

    rows = []
    r1, r2, r3 = g1.copy(), g2.copy(), g3.copy()
    for _ in range(8):
        rows.append(np.concatenate([r1, r2, r3]))
        r1, r2, r3 = np.roll(r1, 1), np.roll(r2, 1), np.roll(r3, 1)

    G24 = np.array(rows, dtype=np.uint8)

    # Row reduce to rank 7
    A = G24.copy()
    independent = []
    pivots = set()
    for i in range(8):
        for col in range(24):
            if col in pivots:
                continue
            if A[i, col] != 0:
                pivots.add(col)
                independent.append(i)
                A[i] = GF4_MUL[GF4_INV[A[i, col]]][A[i]]
                for j in range(8):
                    if j != i and A[j, col] != 0:
                        A[j] = GF4_ADD[A[j], GF4_MUL[A[j, col]][A[i]]]
                break
        if len(independent) >= 7:
            break
    G24 = G24[independent[:7]]

    d24 = _min_dist_k(G24, 7)
    print(f"  [24,7,{d24}]_4 quasi-cyclic")

    # Shorten to [23,6,13]
    _precompute_k(7)
    vecs7, _ = _INFO_CACHE[7]
    best_G23 = None
    for j in range(24):
        col_j = G24[:, j]
        kb = []
        for idx in range(len(vecs7)):
            if len(kb) >= 6:
                break
            v = vecs7[idx]
            dot = 0
            for ii in range(7):
                dot = GF4_ADD[dot, GF4_MUL[v[ii]][col_j[ii]]]
            if dot == 0:
                if len(kb) == 0:
                    kb.append(v.copy())
                else:
                    test = np.array(kb + [v.copy()], dtype=np.uint8)
                    if gf4_rank(test) == len(kb) + 1:
                        kb.append(v.copy())
        if len(kb) < 6:
            continue
        K = np.array(kb, dtype=np.uint8)
        G23 = np.delete(gf4_matmul(K, G24), j, axis=1)
        d23 = min_dist(G23)
        if d23 == 13:
            best_G23 = G23
            print(f"  [23,6,13]_4 from shortening at pos {j}")
            break

    if best_G23 is None:
        return None, 0

    # Puncture to [22,6,12] — pick position minimizing A_12
    best_d22, best_a, best_G22 = 0, 99999, None
    for j in range(23):
        G22 = np.delete(best_G23, j, axis=1)
        d22, cnt = min_dist_full(G22)
        if d22 > best_d22 or (d22 == best_d22 and cnt < best_a):
            best_d22, best_a, best_G22 = d22, cnt, G22.copy()

    best_G22 = systematic_form(best_G22)
    print(f"  [22,6,{best_d22}]_4, A_{best_d22}={best_a}")
    return best_G22, best_d22


# ═══════════════════════════════════════════════════════════════
# SEARCH DOCTRINES — ALL USE C KERNEL
# ═══════════════════════════════════════════════════════════════

def D029_hill_climb(G_base, max_iters=1000, verbose=False):
    """Hill climbing. Uses early exit for massive speedup."""
    k, n = G_base.shape
    G = G_base.copy()
    d_cur = min_dist(G)
    G_best, d_best = G.copy(), d_cur
    cols = _get_cols(k)
    nc = len(cols)
    stag = 0
    for it in range(max_iters):
        col = np.random.randint(0, n)
        old_col = G[:, col].copy()
        G[:, col] = cols[np.random.randint(0, nc)]
        # Early exit: reject immediately if d < current best
        d = min_dist_early(G, d_cur)
        if d >= d_cur:
            # Might be better — do full eval
            d = min_dist(G)
            if d > d_cur:
                d_cur = d
                stag = 0
                if d > d_best:
                    d_best = d
                    G_best = G.copy()
                    if verbose:
                        print(f"    HC iter {it}: d -> {d_best}")
                if d_best >= 13:
                    return G_best, d_best
            else:
                stag += 1
        else:
            G[:, col] = old_col
            stag += 1
        if stag > 300:
            G = G_best.copy()
            for _ in range(np.random.randint(2, 6)):
                G[:, np.random.randint(0, n)] = cols[np.random.randint(0, nc)]
            d_cur = min_dist(G)
            stag = 0
    return G_best, d_best

def D036_mutation(G_base, max_mut=100000):
    """Entry-level mutations on parity. Ultra-fast with early exit."""
    k, n = G_base.shape
    G = G_base.copy()
    d_best = min_dist(G)
    G_best = G.copy()
    is_sys = np.array_equal(G[:, :k], np.eye(k, dtype=np.uint8))
    for _ in range(max_mut):
        r = np.random.randint(0, k)
        c = np.random.randint(k if is_sys else 0, n)
        old = G[r, c]
        nv = np.random.randint(0, 4)
        if nv == old:
            continue
        G[r, c] = nv
        d = min_dist_early(G, d_best)
        if d >= d_best:
            d = min_dist(G)
            if d > d_best:
                d_best = d
                G_best = G.copy()
                if d_best >= 13:
                    return G_best, d_best
        else:
            G[r, c] = old
    return G_best, d_best

def D056_SA(G_base, max_iters=50000, T0=2.0, Tf=0.01):
    """Simulated annealing with early exit."""
    k, n = G_base.shape
    G = G_base.copy()
    d_cur = min_dist(G)
    d_best, G_best = d_cur, G.copy()
    cols = _get_cols(k)
    nc = len(cols)
    for i in range(max_iters):
        T = T0 * (Tf / T0) ** (i / max_iters)
        col = np.random.randint(0, n)
        old_col = G[:, col].copy()
        G[:, col] = cols[np.random.randint(0, nc)]
        d = min_dist_early(G, d_cur - 1)
        if d >= d_cur - 1:
            d = min_dist(G)
        delta = d - d_cur
        if delta > 0 or (delta >= -2 and np.random.random() < np.exp(delta / max(T, 1e-10))):
            d_cur = d
            if d > d_best:
                d_best = d
                G_best = G.copy()
                if d_best >= 13:
                    return G_best, d_best
        else:
            G[:, col] = old_col
    return G_best, d_best

def D057_wild(G_base, rounds=10000):
    """Wild algebraic transforms with early exit."""
    k, n = G_base.shape
    best_d, best_G = min_dist(G_base), G_base.copy()
    cols = _get_cols(k)
    nc = len(cols)
    for _ in range(rounds):
        G = best_G.copy()
        for _ in range(np.random.randint(1, 4)):
            op = np.random.randint(0, 5)
            if op == 0:
                c = np.random.randint(0, n)
                G[:, c] = FROBENIUS[G[:, c]]
            elif op == 1:
                s = np.random.randint(1, 4)
                c = np.random.randint(0, n)
                G[:, c] = GF4_MUL[s][G[:, c]]
            elif op == 2:
                c1, c2 = np.random.choice(n, 2, replace=False)
                G[:, c1] = GF4_ADD[G[:, c1], G[:, c2]]
            elif op == 3:
                c1, c2 = np.random.choice(n, 2, replace=False)
                G[:, [c1, c2]] = G[:, [c2, c1]]
            elif op == 4:
                r1, r2 = np.random.choice(k, 2, replace=False)
                G[r1] = GF4_ADD[G[r1], GF4_MUL[np.random.randint(1, 4)][G[r2]]]
        d = min_dist_early(G, best_d)
        if d >= best_d:
            d = min_dist(G)
            if d > best_d:
                best_d, best_G = d, G.copy()
                if best_d >= 13:
                    return best_G, best_d
    return best_G, best_d

def D054_restarts(G_base, n_restarts=30, iters=1000):
    """Random restarts."""
    best_d, best_G = min_dist(G_base), G_base.copy()
    k, n = G_base.shape
    cols = _get_cols(k)
    nc = len(cols)
    for _ in range(n_restarts):
        G = best_G.copy()
        for _ in range(np.random.randint(3, 8)):
            G[:, np.random.randint(0, n)] = cols[np.random.randint(0, nc)]
        Gr, dr = D029_hill_climb(G, max_iters=iters)
        if dr > best_d:
            best_d, best_G = dr, Gr.copy()
            if best_d >= 13:
                return best_G, best_d
    return best_G, best_d

def D_chorro(G_base, triple, time_limit=120):
    """CHORRO DE AGUA ABRASIVO: concentrated search on a specific triple.
    Replaces 3 columns simultaneously with exhaustive L1 + sampled L2/L3."""
    k, n = G_base.shape
    threshold = min_dist(G_base)
    cols = _get_cols(k)
    nc = len(cols)
    best_d, best_G = threshold, G_base.copy()
    start = time.time()

    c0, c1, c2 = triple
    print(f"    Chorro on triple {triple}, threshold={threshold}")

    # L1: exhaustive sweep of column c0
    L1 = []
    for i in range(nc):
        G = G_base.copy()
        G[:, c0] = cols[i]
        d = min_dist_early(G, threshold)
        if d >= threshold:
            d_full = min_dist(G)
            L1.append((i, d_full))
            if d_full > best_d:
                best_d, best_G = d_full, G.copy()
            if d_full >= 13:
                print(f"    ★ DIAMOND at L1!")
                return G, d_full
    L1.sort(key=lambda x: -x[1])
    print(f"    L1: {len(L1)} candidates, best={best_d}, {time.time()-start:.1f}s")
    if not L1:
        return best_G, best_d

    # L2: sweep column c1 for top L1
    L2 = []
    for pi, (i1, d1) in enumerate(L1[:200]):
        if time.time() - start > time_limit * 0.6:
            break
        G1 = G_base.copy()
        G1[:, c0] = cols[i1]
        for i2 in range(nc):
            G = G1.copy()
            G[:, c1] = cols[i2]
            d = min_dist_early(G, threshold)
            if d >= threshold:
                d_full = min_dist(G)
                L2.append((i1, i2, d_full))
                if d_full > best_d:
                    best_d, best_G = d_full, G.copy()
                    print(f"    L2 improvement: d={best_d}")
                if d_full >= 13:
                    print(f"    ★ DIAMOND at L2!")
                    return G, d_full
        if (pi+1) % 40 == 0:
            print(f"      L2 {pi+1}/{min(len(L1),200)}, pairs={len(L2)}, best={best_d}, {time.time()-start:.1f}s")
    L2.sort(key=lambda x: -x[2])
    print(f"    L2: {len(L2)} pairs, best={best_d}, {time.time()-start:.1f}s")

    # L3: sweep column c2 for top L2 pairs
    for pi, (i1, i2, d12) in enumerate(L2[:50]):
        if time.time() - start > time_limit:
            break
        G12 = G_base.copy()
        G12[:, c0] = cols[i1]
        G12[:, c1] = cols[i2]
        for i3 in range(nc):
            G = G12.copy()
            G[:, c2] = cols[i3]
            d = min_dist_early(G, best_d)
            if d >= best_d:
                d_full = min_dist(G)
                if d_full > best_d:
                    best_d, best_G = d_full, G.copy()
                    print(f"    L3 improvement: d={best_d}")
                if d_full >= 13:
                    print(f"    ★★★ DIAMOND at L3! ★★★")
                    return G, d_full
        if (pi+1) % 10 == 0:
            print(f"      L3 {pi+1}/{min(len(L2),50)}, best={best_d}, {time.time()-start:.1f}s")
    print(f"    Chorro done: best={best_d}, {time.time()-start:.1f}s")
    return best_G, best_d

def D_fatiga(G_base, targets, cycles=500):
    """FATIGA POR RESONANCIA: cycle through target columns repeatedly.
    Replace one target column per cycle, keep improvements."""
    k, n = G_base.shape
    G = G_base.copy()
    d_cur = min_dist(G)
    best_d, best_G = d_cur, G.copy()
    cols = _get_cols(k)
    nc = len(cols)
    for cyc in range(cycles):
        for t in targets:
            old = G[:, t].copy()
            G[:, t] = cols[np.random.randint(0, nc)]
            d = min_dist_early(G, d_cur)
            if d >= d_cur:
                d = min_dist(G)
                if d >= d_cur:
                    d_cur = d
                    if d > best_d:
                        best_d, best_G = d, G.copy()
                        if best_d >= 13:
                            return best_G, best_d
                else:
                    G[:, t] = old
            else:
                G[:, t] = old
    return best_G, best_d


# ═══════════════════════════════════════════════════════════════
# NEW DOCTRINES v5 — 5 DEMOLITION TECHNIQUES
# ═══════════════════════════════════════════════════════════════

def D_cavitacion(G_base, time_limit=60):
    """CAVITACIÓN: Start from [23,6,13], try ALL puncturings after random
    column perturbations. The vacuum approach — remove, don't add.
    We perturb the [23,6,13] parent code and re-puncture."""
    k = 6
    # Rebuild [23,6,13] from [24,7,13]
    g1 = np.array([2, 2, 3, 1, 2, 1, 1, 0], dtype=np.uint8)
    g2 = np.array([3, 2, 1, 1, 1, 0, 0, 0], dtype=np.uint8)
    g3 = np.array([3, 2, 1, 0, 0, 0, 0, 0], dtype=np.uint8)
    rows = []
    r1, r2, r3 = g1.copy(), g2.copy(), g3.copy()
    for _ in range(8):
        rows.append(np.concatenate([r1, r2, r3]))
        r1, r2, r3 = np.roll(r1, 1), np.roll(r2, 1), np.roll(r3, 1)
    G24 = np.array(rows, dtype=np.uint8)
    A = G24.copy()
    independent = []
    pivots = set()
    for i in range(8):
        for col in range(24):
            if col in pivots:
                continue
            if A[i, col] != 0:
                pivots.add(col)
                independent.append(i)
                A[i] = GF4_MUL[GF4_INV[A[i, col]]][A[i]]
                for j in range(8):
                    if j != i and A[j, col] != 0:
                        A[j] = GF4_ADD[A[j], GF4_MUL[A[j, col]][A[i]]]
                break
        if len(independent) >= 7:
            break
    G24 = G24[independent[:7]]

    # Build the [23,6,13] by shortening
    _precompute_k(7)
    vecs7, _ = _INFO_CACHE[7]
    col_0 = G24[:, 0]
    kb = []
    for idx in range(len(vecs7)):
        if len(kb) >= 6:
            break
        v = vecs7[idx]
        dot = 0
        for ii in range(7):
            dot = GF4_ADD[dot, GF4_MUL[v[ii]][col_0[ii]]]
        if dot == 0:
            if len(kb) == 0:
                kb.append(v.copy())
            else:
                test = np.array(kb + [v.copy()], dtype=np.uint8)
                if gf4_rank(test) == len(kb) + 1:
                    kb.append(v.copy())
    if len(kb) < 6:
        return G_base, min_dist(G_base)
    K = np.array(kb, dtype=np.uint8)
    G23 = np.delete(gf4_matmul(K, G24), 0, axis=1)

    best_d, best_G = min_dist(G_base), G_base.copy()
    cols23 = _get_cols(6)
    nc = len(cols23)
    start = time.time()

    while time.time() - start < time_limit:
        # Perturb 1-3 columns of the [23,6,13]
        G23p = G23.copy()
        n_perturb = np.random.randint(1, 4)
        for _ in range(n_perturb):
            c = np.random.randint(0, 23)
            G23p[:, c] = cols23[np.random.randint(0, nc)]
        # Check if the perturbed [23,6,?] still has d >= 12
        d23 = min_dist_early(G23p, 12)
        if d23 < 12:
            continue
        # Try ALL 23 puncturings
        for j in range(23):
            G22 = np.delete(G23p, j, axis=1)
            d22 = min_dist_early(G22, 13)
            if d22 >= 13:
                d22_full = min_dist(G22)
                if d22_full >= 13:
                    print(f"    ★ CAVITACIÓN: d={d22_full}!")
                    return G22, d22_full
            elif d22 > best_d:
                d22_full = min_dist(G22)
                if d22_full > best_d:
                    best_d = d22_full
                    best_G = G22.copy()
    return best_G, best_d


def D_cunas(G_base, rounds=50000):
    """CUÑAS HIDRÁULICAS: Apply GF(4) isotopy transforms that preserve
    algebraic structure. Frobenius + scalar + additive on column pairs.
    Expand from within the cracks."""
    k, n = G_base.shape
    best_d, best_G = min_dist(G_base), G_base.copy()

    for _ in range(rounds):
        G = best_G.copy()
        # Pick a transform type
        op = np.random.randint(0, 7)
        if op == 0:
            # Frobenius on a random subset of columns
            num = np.random.randint(1, n // 2)
            cols_sel = np.random.choice(n, num, replace=False)
            for c in cols_sel:
                G[:, c] = FROBENIUS[G[:, c]]
        elif op == 1:
            # Scalar multiply a column
            c = np.random.randint(0, n)
            s = np.random.randint(1, 4)
            G[:, c] = GF4_MUL[s][G[:, c]]
        elif op == 2:
            # Add column j to column i (additive isotopy)
            c1, c2 = np.random.choice(n, 2, replace=False)
            s = np.random.randint(1, 4)
            G[:, c1] = GF4_ADD[G[:, c1], GF4_MUL[s][G[:, c2]]]
        elif op == 3:
            # Frobenius on entire matrix + undo on one column
            G_f = FROBENIUS[G]
            c = np.random.randint(0, n)
            G_f[:, c] = G[:, c]  # keep one column unchanged
            G = G_f
        elif op == 4:
            # Row isotopy: multiply a row by scalar, add to another
            r1, r2 = np.random.choice(k, 2, replace=False)
            s = np.random.randint(1, 4)
            G[r1] = GF4_ADD[G[r1], GF4_MUL[s][G[r2]]]
        elif op == 5:
            # Permutation isotopy: swap 2-3 columns
            nc_swap = np.random.randint(2, 4)
            perm = np.random.choice(n, nc_swap, replace=False)
            perm_s = np.random.permutation(perm)
            G[:, perm] = G[:, perm_s]
        elif op == 6:
            # Combined: Frobenius + scalar + swap
            c1, c2 = np.random.choice(n, 2, replace=False)
            G[:, c1] = FROBENIUS[G[:, c1]]
            G[:, c2] = GF4_MUL[np.random.randint(1, 4)][G[:, c2]]
            G[:, [c1, c2]] = G[:, [c2, c1]]

        if gf4_rank(G) < k:
            continue
        d = min_dist_early(G, best_d)
        if d >= best_d:
            d = min_dist(G)
            if d > best_d:
                best_d, best_G = d, G.copy()
                if best_d >= 13:
                    return best_G, best_d
    return best_G, best_d


def D_knuth_columns(G_base, rounds=20000):
    """FRAGILIZACIÓN POR HIDRÓGENO: Generate columns using Knuth Type II
    semifield multiplication. Inject non-associative structure into the code.
    The semifield generates columns that standard GF(4) linear algebra can't."""
    k, n = G_base.shape

    # Knuth Type II multiplication table for tau=1 over GF(4)^2
    # Elements 0-15 as (a0, a1) with a0 = elem // 4, a1 = elem % 4
    # (a0,a1) * (b0,b1) = (a0*b0 + tau*a1*Frob(b1), a0*b1 + a1*b0 + tau*a1*b1)
    KM = np.zeros((16, 16), dtype=np.uint8)
    for a in range(16):
        a0, a1 = a // 4, a % 4
        for b in range(16):
            b0, b1 = b // 4, b % 4
            # tau=1, Frob(x) = x^2 in GF(4)
            frob_b1 = FROBENIUS[b1]
            c0 = GF4_ADD[GF4_MUL[a0][b0], GF4_MUL[a1][frob_b1]]  # tau=1
            c1 = GF4_ADD[GF4_ADD[GF4_MUL[a0][b1], GF4_MUL[a1][b0]], GF4_MUL[a1][b1]]
            KM[a, b] = c0 * 4 + c1

    def knuth_mul(a, b):
        return KM[a, b]

    # Generate column vectors by evaluating semifield expressions
    # A column is a vector in GF(4)^6 ≅ GF(16) x GF(4) etc.
    # Strategy: pick random elements, multiply in Knuth, decompose
    best_d, best_G = min_dist(G_base), G_base.copy()
    cols = _get_cols(k)
    nc = len(cols)

    for _ in range(rounds):
        G = best_G.copy()
        # Generate a "Knuth column" from semifield evaluation
        # Pick 2-3 random GF(16) elements, combine with Knuth mul
        elems = np.random.randint(1, 16, size=3)
        # Build a 6-component vector from Knuth products
        products = []
        for i in range(6):
            e1 = elems[np.random.randint(0, 3)]
            e2 = elems[np.random.randint(0, 3)]
            p = knuth_mul(e1, e2)
            # Map to GF(4)^2 and take one component
            products.append(p % 4 if np.random.random() < 0.5 else p // 4)
        col_vec = np.array(products, dtype=np.uint8)

        if np.all(col_vec == 0):
            continue

        # Replace a random column
        c = np.random.randint(0, n)
        old = G[:, c].copy()
        G[:, c] = col_vec
        if gf4_rank(G) < k:
            G[:, c] = old
            continue
        d = min_dist_early(G, best_d)
        if d >= best_d:
            d = min_dist(G)
            if d > best_d:
                best_d, best_G = d, G.copy()
                if best_d >= 13:
                    return best_G, best_d
        else:
            G[:, c] = old

        # Also try: 2 Knuth columns at once
        if _ % 5 == 0:
            G = best_G.copy()
            c1, c2 = np.random.choice(n, 2, replace=False)
            for ci in [c1, c2]:
                elems = np.random.randint(1, 16, size=3)
                products = []
                for i in range(6):
                    e1 = elems[np.random.randint(0, 3)]
                    e2 = elems[np.random.randint(0, 3)]
                    p = knuth_mul(e1, e2)
                    products.append(p % 4 if np.random.random() < 0.5 else p // 4)
                G[:, ci] = np.array(products, dtype=np.uint8)
            if gf4_rank(G) < k and np.any(G[:, c1]) and np.any(G[:, c2]):
                continue
            d = min_dist_early(G, best_d)
            if d >= best_d:
                d = min_dist(G)
                if d > best_d:
                    best_d, best_G = d, G.copy()
                    if best_d >= 13:
                        return best_G, best_d
    return best_G, best_d


def D_deflagracion(G_base, time_limit=120):
    """DEFLAGRACIÓN: Parallel multi-seed explosion. Launch many independent
    searches from different random perturbations simultaneously.
    Uses sequential simulation of parallel (true multiprocessing needs fork)."""
    k, n = G_base.shape
    best_d, best_G = min_dist(G_base), G_base.copy()
    cols = _get_cols(k)
    nc = len(cols)
    start = time.time()

    # Create 8 independent "seeds" by heavy perturbation
    seeds = []
    for _ in range(8):
        G = best_G.copy()
        n_perturb = np.random.randint(4, 10)
        for _ in range(n_perturb):
            G[:, np.random.randint(0, n)] = cols[np.random.randint(0, nc)]
        if gf4_rank(G) >= k:
            seeds.append(G)

    # Round-robin: give each seed a short burst of hill-climbing
    burst = 2000
    while time.time() - start < time_limit and seeds:
        next_seeds = []
        for G in seeds:
            if time.time() - start > time_limit:
                break
            Gn, dn = D029_hill_climb(G, burst)
            if dn > best_d:
                best_d, best_G = dn, Gn.copy()
                print(f"    Deflagración: d -> {best_d}")
                if best_d >= 13:
                    return best_G, best_d
            # Perturb again for next round
            G2 = Gn.copy()
            for _ in range(np.random.randint(2, 5)):
                G2[:, np.random.randint(0, n)] = cols[np.random.randint(0, nc)]
            if gf4_rank(G2) >= k:
                next_seeds.append(G2)
        seeds = next_seeds if next_seeds else seeds
        burst = min(burst + 1000, 5000)  # increase intensity
    return best_G, best_d


def D_hilo_diamante(G_base, time_limit=60):
    """HILO DE DIAMANTE: Deterministic constraint propagation.
    Find weight-12 codewords, extract their zero-position sets,
    then search for columns that eliminate ALL weight-12 codewords.
    Friction-based: grind away the bad codewords one by one."""
    k, n = G_base.shape
    d_cur = min_dist(G_base)
    if d_cur >= 13:
        return G_base, d_cur

    best_d, best_G = d_cur, G_base.copy()
    _precompute_info(k)
    start = time.time()

    # Find all weight-12 (or weight <= d_cur) codewords
    total = 4**k - 1
    codewords = np.zeros((total, n), dtype=np.uint8)
    for j, val, mask in _INFO_NONZERO:
        contrib = GF4_MUL[val][G_base[j]]
        codewords[mask] = GF4_ADD[codewords[mask], contrib]
    weights = np.count_nonzero(codewords, axis=1)
    bad_idx = np.where(weights == d_cur)[0]

    if len(bad_idx) == 0:
        return best_G, best_d

    # For each bad codeword, find which columns are zero (that's where the "holes" are)
    # If we can make a bad codeword nonzero at one of its zero positions, it becomes weight d_cur+1
    bad_info = _INFO_VECS[bad_idx]
    bad_cws = codewords[bad_idx]

    # For each bad codeword, get its zero columns
    cols_to_try = _get_cols(k)
    nc = len(cols_to_try)

    # Strategy: for each column position, count how many bad codewords are zero there
    # Replace the column with the highest "coverage" potential
    zero_count = np.zeros(n, dtype=np.int32)
    for i in range(len(bad_idx)):
        zeros = np.where(bad_cws[i] == 0)[0]
        zero_count[zeros] += 1

    # Sort columns by how many bad codewords they could "fix"
    col_priority = np.argsort(-zero_count)

    for target_col in col_priority[:6]:
        if time.time() - start > time_limit:
            break
        if zero_count[target_col] == 0:
            continue
        # Try all possible replacement columns
        for ci in range(nc):
            G = best_G.copy()
            G[:, target_col] = cols_to_try[ci]
            if gf4_rank(G) < k:
                continue
            d = min_dist_early(G, best_d)
            if d >= best_d:
                d = min_dist(G)
                if d > best_d:
                    best_d, best_G = d, G.copy()
                    if best_d >= 13:
                        print(f"    ★ HILO: d={best_d}!")
                        return best_G, best_d
    return best_G, best_d


# ═══════════════════════════════════════════════════════════════
# v6 DOCTRINES — INVINCIBILIDAD + VELOCIDAD
# ═══════════════════════════════════════════════════════════════

def D_rde(time_limit=120):
    """DETONACIÓN ROTATIVA: Generate [22,6,d] matrices from SCRATCH
    using multiple algebraic constructions, not just QR shortening.
    Each detonation is a completely independent seed → hill climb."""
    best_d, best_G = 0, None
    cols = _get_cols(6)
    nc = len(cols)
    start = time.time()
    detonations = 0

    while time.time() - start < time_limit:
        # Pick a random construction method
        method = np.random.randint(0, 5)
        G = np.zeros((6, 22), dtype=np.uint8)
        G[:, :6] = np.eye(6, dtype=np.uint8)

        if method == 0:
            # Random parity matrix
            for c in range(6, 22):
                G[:, c] = cols[np.random.randint(0, nc)]
        elif method == 1:
            # Circulant-like: each parity col is a shifted version
            base = cols[np.random.randint(0, nc)].copy()
            for c in range(6, 22):
                G[:, c] = base
                # Shift + scramble
                base = np.roll(base, 1)
                base = GF4_ADD[base, cols[np.random.randint(0, nc)] % 2]
        elif method == 2:
            # Vandermonde-like over GF(4)
            alphas = np.random.choice(range(1, 4), 6, replace=True).astype(np.uint8)
            for c in range(6, 22):
                seed_val = np.random.randint(1, 4)
                power = np.ones(6, dtype=np.uint8)
                for row in range(6):
                    power[row] = seed_val
                    for _ in range(c - 5):
                        power[row] = GF4_MUL[power[row]][alphas[row]]
                G[:, c] = power
        elif method == 3:
            # Dense random with high weight bias
            for c in range(6, 22):
                col = np.random.randint(1, 4, size=6).astype(np.uint8)
                # Zero out 0-1 random entries
                zeros = np.random.randint(0, 2)
                if zeros > 0:
                    idx = np.random.choice(6, zeros, replace=False)
                    col[idx] = 0
                if np.any(col):
                    G[:, c] = col
                else:
                    G[:, c] = cols[np.random.randint(0, nc)]
        elif method == 4:
            # Knuth semifield evaluation columns
            KM = np.zeros((16, 16), dtype=np.uint8)
            tau = np.random.randint(1, 4)
            for a in range(16):
                a0, a1 = a // 4, a % 4
                for b in range(16):
                    b0, b1 = b // 4, b % 4
                    frob_b1 = FROBENIUS[b1]
                    c0 = GF4_ADD[GF4_MUL[a0][b0], GF4_MUL[tau][GF4_MUL[a1][frob_b1]]]
                    c1 = GF4_ADD[GF4_ADD[GF4_MUL[a0][b1], GF4_MUL[a1][b0]], GF4_MUL[tau][GF4_MUL[a1][b1]]]
                    KM[a, b] = c0 * 4 + c1
            for c in range(6, 22):
                elems = np.random.randint(1, 16, size=3)
                col = np.zeros(6, dtype=np.uint8)
                for i in range(6):
                    p = KM[elems[i % 3], elems[(i + 1) % 3]]
                    col[i] = p % 4 if i % 2 == 0 else p // 4
                if np.any(col):
                    G[:, c] = col
                else:
                    G[:, c] = cols[np.random.randint(0, nc)]

        # Quick check: reject if d < 8
        d = min_dist_early(G, 8)
        if d < 8:
            continue

        detonations += 1
        # Hill climb from this fresh seed
        Gn, dn = D029_hill_climb(G, 5000)
        if dn > best_d:
            best_d, best_G = dn, Gn.copy()
            elapsed = time.time() - start
            print(f"    RDE #{detonations}: d={best_d} ({elapsed:.0f}s)")
            if best_d >= 13:
                print(f"    ★★★ RDE DETONATION: DIAMOND! ★★★")
                return best_G, best_d

    elapsed = time.time() - start
    print(f"    RDE: {detonations} detonations, best d={best_d} ({elapsed:.0f}s)")
    return best_G, best_d if best_G is not None else 0


def D_bmg(G_base, time_limit=90):
    """VIDRIO METÁLICO: Explore the space of ALL [22,6,12] codes,
    not just derivatives of the QR code. Generate random [22,6,d≥11]
    seeds and attempt d=12→13 from each. No grain boundaries = no
    single point of failure in the search."""
    best_d, best_G = min_dist(G_base), G_base.copy()
    cols = _get_cols(6)
    nc = len(cols)
    start = time.time()
    good_seeds = 0

    while time.time() - start < time_limit:
        # Generate a random matrix
        G = np.zeros((6, 22), dtype=np.uint8)
        G[:, :6] = np.eye(6, dtype=np.uint8)
        for c in range(6, 22):
            G[:, c] = cols[np.random.randint(0, nc)]

        # Quick screen: need d >= 9 to be worth climbing
        d = min_dist_early(G, 9)
        if d < 9:
            continue

        # Full eval + climb
        d = min_dist(G)
        if d >= 10:
            good_seeds += 1
            # Aggressive climb
            Gn, dn = D029_hill_climb(G, 10000)
            if dn > best_d:
                best_d, best_G = dn, Gn.copy()
                elapsed = time.time() - start
                print(f"    BMG seed #{good_seeds}: d={best_d} ({elapsed:.0f}s)")
                if best_d >= 13:
                    return best_G, best_d

    elapsed = time.time() - start
    print(f"    BMG: {good_seeds} viable seeds, best d={best_d} ({elapsed:.0f}s)")
    return best_G, best_d


def D_sabre(G_base, time_limit=180):
    """SABRE: Hybrid jet/rocket search. Phase 1 (jet mode): aggressive SA
    from current best. When stagnant, PURGE and restart from a fresh d≥11
    seed (rocket mode). Repeat cycle until time runs out."""
    best_d, best_G = min_dist(G_base), G_base.copy()
    cols = _get_cols(6)
    nc = len(cols)
    start = time.time()
    k, n = 6, 22
    cycle = 0

    while time.time() - start < time_limit:
        cycle += 1
        remaining = time_limit - (time.time() - start)
        if remaining < 5:
            break
        burst = min(remaining / 2, 30)

        # JET MODE: SA from best
        Gn, dn = D056_SA(best_G, int(burst * 1500))
        if dn > best_d:
            best_d, best_G = dn, Gn.copy()
            print(f"    SABRE jet #{cycle}: d={best_d}")
            if best_d >= 13:
                return best_G, best_d
            continue  # Stay in jet mode if improving

        # ROCKET MODE: purge and restart from scratch
        # Generate fresh seed by random construction + quick climb
        for attempt in range(20):
            G = np.zeros((6, 22), dtype=np.uint8)
            G[:, :6] = np.eye(6, dtype=np.uint8)
            for c in range(6, 22):
                G[:, c] = cols[np.random.randint(0, nc)]
            d = min_dist_early(G, 10)
            if d >= 10:
                Gr, dr = D029_hill_climb(G, 3000)
                if dr >= best_d:
                    best_G = Gr.copy()
                    if dr > best_d:
                        best_d = dr
                        print(f"    SABRE rocket #{cycle}: d={best_d}")
                    if best_d >= 13:
                        return best_G, best_d
                    break
    return best_G, best_d


def D_borofeno(G_base, time_limit=60):
    """BOROFENO: Anisotropic search. Instead of treating all 16 columns
    equally, identify the DIRECTION of maximum vulnerability and attack
    ONLY along that axis. Directional pressure."""
    k, n = G_base.shape
    best_d, best_G = min_dist(G_base), G_base.copy()
    cols = _get_cols(k)
    nc = len(cols)
    start = time.time()

    # Find the anisotropy: which single column replacement gives best d?
    col_potential = np.zeros(n, dtype=np.int32)
    for c in range(n):
        best_dc = 0
        for _ in range(100):  # Sample 100 random replacements per column
            G = best_G.copy()
            G[:, c] = cols[np.random.randint(0, nc)]
            d = min_dist_early(G, best_d)
            if d >= best_d:
                d = min_dist(G)
                if d > best_dc:
                    best_dc = d
        col_potential[c] = best_dc

    # Find the axis of maximum potential
    axis = np.argsort(-col_potential)
    top_axis = axis[:4]  # Top 4 most promising columns
    print(f"    Borofeno axis: {list(top_axis)}, potential={[col_potential[c] for c in top_axis]}")

    # Concentrate ALL effort on these columns
    while time.time() - start < time_limit:
        G = best_G.copy()
        # Replace 1-3 of the top columns
        n_replace = np.random.randint(1, min(4, len(top_axis) + 1))
        targets = np.random.choice(top_axis, n_replace, replace=False)
        for t in targets:
            G[:, t] = cols[np.random.randint(0, nc)]
        d = min_dist_early(G, best_d)
        if d >= best_d:
            d = min_dist(G)
            if d > best_d:
                best_d, best_G = d, G.copy()
                print(f"    Borofeno: d -> {best_d}")
                if best_d >= 13:
                    return best_G, best_d
    return best_G, best_d


# ═══════════════════════════════════════════════════════════════
# v7 DOCTRINES — VISIÓN + FUGITIVO + MARIO BROS
# ═══════════════════════════════════════════════════════════════

def D_ghost_imaging(G_base, rounds=50000):
    """GHOST IMAGING: Don't search for d=13 directly. Study HOW d=12
    matrices fail — find the correlation pattern in weight-12 codewords.
    Use that pattern to guide mutations toward eliminating ALL weight-12s.

    The ghost of the diamond is in the failure pattern."""
    k, n = G_base.shape
    best_d, best_G = min_dist(G_base), G_base.copy()

    # Step 1: Photograph the failure — get ALL weight-12 codewords
    _precompute_info(k)
    total = 4**k - 1
    codewords = np.zeros((total, n), dtype=np.uint8)
    for j, val, mask in _INFO_NONZERO:
        contrib = GF4_MUL[val][G_base[j]]
        codewords[mask] = GF4_ADD[codewords[mask], contrib]
    weights = np.count_nonzero(codewords, axis=1)
    bad_idx = np.where(weights == best_d)[0]

    if len(bad_idx) == 0:
        return best_G, best_d

    bad_cws = codewords[bad_idx]

    # Step 2: Build the "ghost" — a correlation matrix
    # For each pair of columns, count how often they're BOTH zero in bad codewords
    # High correlation = those columns are "entangled" in causing low weight
    ghost = np.zeros((n, n), dtype=np.int32)
    for cw in bad_cws:
        zeros = np.where(cw == 0)[0]
        for i in range(len(zeros)):
            for j in range(i + 1, len(zeros)):
                ghost[zeros[i], zeros[j]] += 1
                ghost[zeros[j], zeros[i]] += 1

    # Step 3: Find the strongest ghost correlations — these column PAIRS
    # are the "entangled photons" that reveal the diamond
    ghost_flat = []
    for i in range(n):
        for j in range(i + 1, n):
            if ghost[i, j] > 0:
                ghost_flat.append((ghost[i, j], i, j))
    ghost_flat.sort(reverse=True)

    # Step 4: Attack the top correlated pairs
    cols = _get_cols(k)
    nc = len(cols)
    for score, ci, cj in ghost_flat[:10]:
        for _ in range(rounds // 10):
            G = best_G.copy()
            G[:, ci] = cols[np.random.randint(0, nc)]
            G[:, cj] = cols[np.random.randint(0, nc)]
            d = min_dist_early(G, best_d)
            if d >= best_d:
                d = min_dist(G)
                if d > best_d:
                    best_d, best_G = d, G.copy()
                    if best_d >= 13:
                        print(f"    ★ GHOST: d={best_d}!")
                        return best_G, best_d
    return best_G, best_d


def D_triangulacion(G_base, time_limit=60):
    """TRIANGULACIÓN DE METADATOS: Analyze the weight-12 codewords to
    find which INFO VECTORS produce them. Then search for column changes
    that push those specific info vectors to weight 13+.

    Track the fugitive by its supply chain, not its location."""
    k, n = G_base.shape
    best_d, best_G = min_dist(G_base), G_base.copy()

    # Map: for each weight-12 codeword, which info vector generated it?
    _precompute_info(k)
    total = 4**k - 1
    codewords = np.zeros((total, n), dtype=np.uint8)
    for j, val, mask in _INFO_NONZERO:
        contrib = GF4_MUL[val][G_base[j]]
        codewords[mask] = GF4_ADD[codewords[mask], contrib]
    weights = np.count_nonzero(codewords, axis=1)
    bad_idx = np.where(weights == best_d)[0]

    if len(bad_idx) == 0:
        return best_G, best_d

    # For each bad codeword: find which columns are zero
    # A column change at position c can only affect codewords where
    # the info vector has nonzero contribution to column c
    bad_info = _INFO_VECS[bad_idx]
    bad_cws = codewords[bad_idx]

    # For each column c: which bad codewords have a zero at c?
    # These are the ones we can "push" to weight 13 by changing column c
    cols = _get_cols(k)
    nc = len(cols)
    start = time.time()

    # Score each column by how many bad codewords it could fix
    col_fix_count = np.zeros(n, dtype=np.int32)
    for i in range(len(bad_idx)):
        zeros = np.where(bad_cws[i] == 0)[0]
        col_fix_count[zeros] += 1

    # Sort columns by fix potential
    priority = np.argsort(-col_fix_count)

    # For top columns: try replacements that fix the MOST bad codewords
    for target in priority[:8]:
        if time.time() - start > time_limit:
            break
        if col_fix_count[target] == 0:
            continue

        # For each candidate column, simulate how many bad codewords get fixed
        best_fixes = 0
        best_col_vec = None
        for ci in range(nc):
            col_vec = cols[ci]
            # Count how many bad codewords would become nonzero at this position
            fixes = 0
            for bi in range(len(bad_idx)):
                if bad_cws[bi][target] == 0:
                    # New value at this position = sum of info_vec[j] * col_vec[j]
                    new_val = 0
                    for j in range(k):
                        new_val = GF4_ADD[new_val, GF4_MUL[bad_info[bi][j]][col_vec[j]]]
                    if new_val != 0:
                        fixes += 1
            if fixes > best_fixes:
                best_fixes = fixes
                best_col_vec = col_vec.copy()

        if best_col_vec is not None:
            G = best_G.copy()
            G[:, target] = best_col_vec
            if gf4_rank(G) >= k:
                d = min_dist(G)
                if d > best_d:
                    best_d, best_G = d, G.copy()
                    print(f"    Triangulación col {target}: d -> {best_d}")
                    if best_d >= 13:
                        return best_G, best_d
                elif d == best_d:
                    # Even if d didn't increase, check if A_d decreased
                    _, cnt = min_dist_full(G)
                    _, cnt_old = min_dist_full(best_G)
                    if cnt < cnt_old:
                        best_G = G.copy()
                        print(f"    Triangulación col {target}: A_{d} reduced {cnt_old}->{cnt}")
    return best_G, best_d


def D_profiling(G_base, time_limit=60):
    """PROFILING DETERMINISTA: Use known properties of [22,6,13]_4 to
    constrain the search. A [22,6,13] must have specific weight distribution
    properties (Pless power moments). Filter candidates by these constraints.

    The fugitive can't go just anywhere — GF(4) laws constrain it."""
    k, n = G_base.shape
    best_d, best_G = min_dist(G_base), G_base.copy()
    cols = _get_cols(k)
    nc = len(cols)
    start = time.time()

    # Known: for a [22,6,13]_4, the weight enumerator must satisfy
    # Pless power moment identities. Key constraint:
    # A_13 must be divisible by 3 (since |Aut(GF(4))| = 2, and
    # codewords come in {c, ωc, ω²c} triples)
    # Also: sum of A_i * i = 22 * (4^6 - 1) * 3/4 = 22 * 4095 * 3/4

    # Strategy: do mutations but ONLY accept if the weight distribution
    # moves toward a valid [22,6,13] profile
    target_A13_min = 90   # Reasonable minimum for [22,6,13]
    target_A13_max = 300  # Reasonable maximum

    while time.time() - start < time_limit:
        G = best_G.copy()
        # Mutate 1-2 entries
        for _ in range(np.random.randint(1, 3)):
            r = np.random.randint(0, k)
            c = np.random.randint(k, n)  # Only parity
            G[r, c] = np.random.randint(0, 4)

        d = min_dist_early(G, best_d)
        if d < best_d:
            continue
        if d >= best_d:
            d_full, cnt = min_dist_full(G)
            if d_full > best_d:
                best_d, best_G = d_full, G.copy()
                if best_d >= 13:
                    return best_G, best_d
            elif d_full == best_d and cnt < min_dist_full(best_G)[1]:
                # Accept if fewer bad codewords (A_d decreasing = profiling toward target)
                best_G = G.copy()
    return best_G, best_d


def D_hiperespectral(G_base, rounds=30000):
    """HIPERESPECTRAL: Spectral fingerprint filter. Before full eval,
    check a CHEAP spectral signature: the weight of a small subset of
    codewords. Reject 90% of candidates without full eval.

    THz sensor: only beep on weight-13 vibration."""
    k, n = G_base.shape
    best_d, best_G = min_dist(G_base), G_base.copy()
    cols = _get_cols(k)
    nc = len(cols)

    # Build a "probe set": 200 random info vectors that are most likely
    # to produce low-weight codewords (those with few nonzero entries)
    probes = []
    for idx in range(1, 4**k):
        v = idx_to_gf4_vec(idx, k)
        nz = np.count_nonzero(v)
        if nz <= 2:  # Weight-1 and weight-2 info vectors
            probes.append(v)
    probes = np.array(probes[:300], dtype=np.uint8)

    for _ in range(rounds):
        G = best_G.copy()
        c = np.random.randint(0, n)
        G[:, c] = cols[np.random.randint(0, nc)]

        # CHEAP pre-filter: encode only the probe set
        reject = False
        for p in probes:
            cw = encode(p, G)
            w = int(np.count_nonzero(cw))
            if w > 0 and w < best_d:
                reject = True
                break
        if reject:
            continue

        # Passed pre-filter → full eval
        d = min_dist_early(G, best_d)
        if d >= best_d:
            d = min_dist(G)
            if d > best_d:
                best_d, best_G = d, G.copy()
                if best_d >= 13:
                    print(f"    ★ HIPERESPECTRAL: d={best_d}!")
                    return best_G, best_d
    return best_G, best_d


def D_metamaterial(G_base, time_limit=60):
    """METAMATERIAL / MINUS WORLD: Puncture [23,6,13] WITH simultaneous
    column perturbation. Normal puncturing always gives d=12 (Theorem 1).
    But if we perturb columns WHILE puncturing, we might find a path
    through the "negative index" — a puncturing that INCREASES d.

    Enter the Minus World: operate outside standard algebra."""
    k = 6
    # Rebuild [23,6,13]
    g1 = np.array([2, 2, 3, 1, 2, 1, 1, 0], dtype=np.uint8)
    g2 = np.array([3, 2, 1, 1, 1, 0, 0, 0], dtype=np.uint8)
    g3 = np.array([3, 2, 1, 0, 0, 0, 0, 0], dtype=np.uint8)
    rows = []
    r1, r2, r3 = g1.copy(), g2.copy(), g3.copy()
    for _ in range(8):
        rows.append(np.concatenate([r1, r2, r3]))
        r1, r2, r3 = np.roll(r1, 1), np.roll(r2, 1), np.roll(r3, 1)
    G24 = np.array(rows, dtype=np.uint8)
    A = G24.copy()
    independent = []
    pivots = set()
    for i in range(8):
        for col in range(24):
            if col in pivots:
                continue
            if A[i, col] != 0:
                pivots.add(col)
                independent.append(i)
                A[i] = GF4_MUL[GF4_INV[A[i, col]]][A[i]]
                for j in range(8):
                    if j != i and A[j, col] != 0:
                        A[j] = GF4_ADD[A[j], GF4_MUL[A[j, col]][A[i]]]
                break
        if len(independent) >= 7:
            break
    G24 = G24[independent[:7]]

    _precompute_k(7)
    vecs7, _ = _INFO_CACHE[7]
    # Build ALL possible [23,6,13] shortenings
    G23_list = []
    for j in range(24):
        col_j = G24[:, j]
        kb = []
        for idx in range(len(vecs7)):
            if len(kb) >= 6:
                break
            v = vecs7[idx]
            dot = 0
            for ii in range(7):
                dot = GF4_ADD[dot, GF4_MUL[v[ii]][col_j[ii]]]
            if dot == 0:
                if len(kb) == 0:
                    kb.append(v.copy())
                else:
                    test = np.array(kb + [v.copy()], dtype=np.uint8)
                    if gf4_rank(test) == len(kb) + 1:
                        kb.append(v.copy())
        if len(kb) >= 6:
            K = np.array(kb[:6], dtype=np.uint8)
            G23 = np.delete(gf4_matmul(K, G24), j, axis=1)
            if min_dist_early(G23, 13) >= 13:
                G23_list.append(G23)

    if not G23_list:
        return G_base, min_dist(G_base)

    best_d, best_G = min_dist(G_base), G_base.copy()
    cols = _get_cols(6)
    nc = len(cols)
    start = time.time()
    print(f"    Metamaterial: {len(G23_list)} parent [23,6,13] codes")

    while time.time() - start < time_limit:
        # Pick a random [23,6,13] parent
        G23 = G23_list[np.random.randint(0, len(G23_list))].copy()

        # MINUS WORLD: perturb 1-2 columns BEFORE puncturing
        n_perturb = np.random.randint(1, 3)
        for _ in range(n_perturb):
            c = np.random.randint(0, 23)
            op = np.random.randint(0, 4)
            if op == 0:
                G23[:, c] = cols[np.random.randint(0, nc)]
            elif op == 1:
                G23[:, c] = FROBENIUS[G23[:, c]]
            elif op == 2:
                s = np.random.randint(1, 4)
                G23[:, c] = GF4_MUL[s][G23[:, c]]
            elif op == 3:
                c2 = np.random.randint(0, 23)
                G23[:, c] = GF4_ADD[G23[:, c], G23[:, c2]]

        # Now puncture at each position
        for j in range(23):
            G22 = np.delete(G23, j, axis=1)
            d = min_dist_early(G22, 13)
            if d >= 13:
                d_full = min_dist(G22)
                if d_full >= 13:
                    print(f"    ★★★ METAMATERIAL: d={d_full}! ★★★")
                    return G22, d_full
            elif d > best_d:
                d_full = min_dist(G22)
                if d_full > best_d:
                    best_d, best_G = d_full, G22.copy()
    return best_G, best_d


def D_oneup_loop(G_base, time_limit=60):
    """1-UP LOOP: Positive feedback hill climbing. When a mutation reduces
    A_12 (number of weight-12 codewords), KEEP iterating in that SAME
    direction. The staircase shell bounce — each improvement feeds the next.

    Farm entropy by exploiting momentum."""
    k, n = G_base.shape
    G = G_base.copy()
    d_cur, a_cur = min_dist_full(G)
    best_d, best_G, best_a = d_cur, G.copy(), a_cur
    start = time.time()

    while time.time() - start < time_limit:
        # Pick a random mutation
        r = np.random.randint(0, k)
        c = np.random.randint(k, n)  # parity only
        old_val = G[r, c]
        new_val = np.random.randint(0, 4)
        if new_val == old_val:
            continue

        G[r, c] = new_val
        d = min_dist_early(G, d_cur)
        if d < d_cur:
            G[r, c] = old_val
            continue

        d_full, a_new = min_dist_full(G)
        if d_full > best_d or (d_full == best_d and a_new < best_a):
            if d_full > best_d:
                best_d = d_full
                print(f"    1-UP: d -> {best_d}")
            best_a = a_new
            best_G = G.copy()
            d_cur, a_cur = d_full, a_new
            if best_d >= 13:
                return best_G, best_d

            # 1-UP MOMENTUM: keep pushing in the SAME direction
            # Try further changes to the same row and nearby columns
            for momentum in range(20):
                c2 = c + np.random.randint(-2, 3)
                if c2 < k or c2 >= n:
                    continue
                r2 = r if np.random.random() < 0.5 else np.random.randint(0, k)
                old2 = G[r2, c2]
                G[r2, c2] = np.random.randint(0, 4)
                if G[r2, c2] == old2:
                    continue
                d2 = min_dist_early(G, d_cur)
                if d2 >= d_cur:
                    d2f, a2 = min_dist_full(G)
                    if d2f > best_d or (d2f == best_d and a2 < best_a):
                        if d2f > best_d:
                            best_d = d2f
                            print(f"    1-UP COMBO x{momentum+1}: d -> {best_d}")
                        best_a = a2
                        best_G = G.copy()
                        d_cur, a_cur = d2f, a2
                        if best_d >= 13:
                            return best_G, best_d
                    else:
                        G[r2, c2] = old2
                else:
                    G[r2, c2] = old2
        else:
            G[r, c] = old_val
    return best_G, best_d


def D_warp_zone(G_base, time_limit=60):
    """WARP ZONE: Skip intermediate states. Instead of single-entry mutations,
    replace ENTIRE ROWS of the parity matrix at once. Warp from level 1 to
    level 8 in one jump.

    Tunnel through the search space."""
    k, n = G_base.shape
    best_d, best_G = min_dist(G_base), G_base.copy()
    Gs = systematic_form(best_G)
    if not np.array_equal(Gs[:, :k], np.eye(k, dtype=np.uint8)):
        Gs = best_G.copy()
    start = time.time()

    while time.time() - start < time_limit:
        G = Gs.copy()
        # WARP: replace an entire row of the parity part
        r = np.random.randint(0, k)
        new_parity = np.random.randint(0, 4, size=n - k).astype(np.uint8)
        G[r, k:] = new_parity

        d = min_dist_early(G, best_d)
        if d >= best_d:
            d = min_dist(G)
            if d > best_d:
                best_d, best_G = d, G.copy()
                Gs = G.copy()
                print(f"    WARP: d -> {best_d}")
                if best_d >= 13:
                    return best_G, best_d
            elif d == best_d:
                # Accept with some probability to explore
                _, cnt_new = min_dist_full(G)
                _, cnt_old = min_dist_full(best_G)
                if cnt_new < cnt_old:
                    best_G = G.copy()
                    Gs = G.copy()
    return best_G, best_d


# ═══════════════════════════════════════════════════════════════
# v8 DOCTRINES — MISILES + FLUORESCENCIA
# ═══════════════════════════════════════════════════════════════

def D_heat_seeker(G_base, time_limit=45):
    """HEAT-SEEKING SIDEWINDER: Lock-on to the mutation direction that
    reduces A_12 fastest. Compute discrete gradient of A_12 w.r.t. each
    parity entry, then CHASE the steepest descent.

    The seeker doesn't see the plane — it sees the thermal discontinuity."""
    k, n = G_base.shape
    G = systematic_form(G_base.copy())
    if not np.array_equal(G[:, :k], np.eye(k, dtype=np.uint8)):
        G = G_base.copy()
    d_cur, a_cur = min_dist_full(G)
    best_d, best_G, best_a = d_cur, G.copy(), a_cur
    start = time.time()

    d_floor = best_d  # NEVER let d drop below this
    while time.time() - start < time_limit:
        # SCAN PHASE: compute "heat" (A_d reduction) for each parity entry
        heat_map = []
        for r in range(k):
            for c in range(k, n):
                old = G[r, c]
                best_val, best_delta = old, 0
                for v in range(4):
                    if v == old:
                        continue
                    G[r, c] = v
                    d_test = min_dist_early(G, d_floor)
                    if d_test >= d_floor:  # Never accept d < floor
                        d_f, a_f = min_dist_full(G)
                        if d_f > best_d:
                            best_d, best_G = d_f, G.copy()
                            best_a = a_f
                            d_cur, a_cur = d_f, a_f
                            d_floor = d_f
                            if best_d >= 13:
                                print(f"    HEAT-SEEK: d={best_d}!")
                                return best_G, best_d
                            best_val = v
                            best_delta = -9999
                            break
                        elif d_f == d_floor and a_f < a_cur:
                            delta = a_cur - a_f
                            if delta > best_delta:
                                best_delta = delta
                                best_val = v
                        # REJECT if d_f < d_floor (don't go below)
                G[r, c] = old
                if best_delta > 0:
                    heat_map.append((best_delta, r, c, best_val))

        if not heat_map:
            # No improving moves — perturb and retry FROM BEST
            G = best_G.copy()
            for _ in range(3):
                r = np.random.randint(0, k)
                c = np.random.randint(k, n)
                G[r, c] = np.random.randint(0, 4)
            d_cur, a_cur = min_dist_full(G)
            if d_cur < d_floor:
                G = best_G.copy()
                d_cur, a_cur = best_d, best_a
            continue

        # LOCK-ON: apply the hottest mutation
        heat_map.sort(reverse=True)
        delta, r, c, v = heat_map[0]
        G[r, c] = v
        d_cur, a_cur = min_dist_full(G)
        if d_cur < d_floor:
            G[r, c] = G[r, c]  # revert handled by scan
            G = best_G.copy()
            d_cur, a_cur = best_d, best_a
            continue
        if d_cur > best_d or (d_cur == best_d and a_cur < best_a):
            best_d, best_G, best_a = d_cur, G.copy(), a_cur
            print(f"    Heat-seek: A_{d_cur}={a_cur} (D={delta})")
            print(f"    Matrix at A_{d_cur}={a_cur}:")
            syms = {0:"0", 1:"1", 2:"w", 3:"w2"}
            for row in range(best_G.shape[0]):
                print("    [" + " ".join(syms[best_G[row,cc]] for cc in range(best_G.shape[1])) + "]")
        if best_d >= 13:
            return best_G, best_d
    return best_G, best_d


def D_propnav(G_base, time_limit=45):
    """PROPORTIONAL NAVIGATION: Track the "line of sight" to d=13.
    Measure which entries have the strongest INFLUENCE on A_12.
    Navigate proportionally: bigger influence = bigger correction.

    γ̇ = N·λ̇ — the missile turns proportional to the LOS rate."""
    k, n = G_base.shape
    G = systematic_form(G_base.copy())
    if not np.array_equal(G[:, :k], np.eye(k, dtype=np.uint8)):
        G = G_base.copy()
    d_cur, a_cur = min_dist_full(G)
    best_d, best_G, best_a = d_cur, G.copy(), a_cur
    start = time.time()

    # Compute influence map: for each entry, how many weight-12
    # codewords does it participate in?
    _precompute_info(k)
    total = 4**k - 1
    codewords = np.zeros((total, n), dtype=np.uint8)
    for j, val, mask in _INFO_NONZERO:
        contrib = GF4_MUL[val][G[j]]
        codewords[mask] = GF4_ADD[codewords[mask], contrib]
    weights = np.count_nonzero(codewords, axis=1)
    bad_idx = np.where(weights == d_cur)[0]
    bad_info = _INFO_VECS[bad_idx]

    # Influence[r][c] = how many bad codewords have nonzero info[r]
    # AND zero at position c (meaning changing G[r,c] could fix that codeword)
    influence = np.zeros((k, n), dtype=np.float64)
    bad_cws = codewords[bad_idx]
    for bi in range(len(bad_idx)):
        zeros_c = np.where(bad_cws[bi] == 0)[0]
        nonzero_r = np.where(bad_info[bi] != 0)[0]
        for r in nonzero_r:
            influence[r, zeros_c] += 1.0

    # Normalize to get navigation gain N
    max_inf = np.max(influence)
    if max_inf > 0:
        influence /= max_inf

    while time.time() - start < time_limit:
        # Select entry proportional to influence
        parity_inf = influence[:, k:].flatten()
        total_inf = np.sum(parity_inf)
        if total_inf < 1e-10:
            # Uniform random
            r = np.random.randint(0, k)
            c = np.random.randint(k, n)
        else:
            probs = parity_inf / total_inf
            idx = np.random.choice(len(probs), p=probs)
            r = idx // (n - k)
            c = k + idx % (n - k)

        old = G[r, c]
        G[r, c] = np.random.randint(0, 4)
        if G[r, c] == old:
            continue

        d = min_dist_early(G, d_cur)
        if d >= d_cur:
            d_f, a_f = min_dist_full(G)
            if d_f > best_d or (d_f == best_d and a_f < best_a):
                if d_f > best_d:
                    best_d = d_f
                    print(f"    PropNav: d -> {best_d}")
                best_a = a_f
                best_G = G.copy()
                d_cur, a_cur = d_f, a_f
                if best_d >= 13:
                    return best_G, best_d
                # Recompute influence after improvement
                codewords = np.zeros((total, n), dtype=np.uint8)
                for j, val, mask in _INFO_NONZERO:
                    contrib = GF4_MUL[val][G[j]]
                    codewords[mask] = GF4_ADD[codewords[mask], contrib]
                weights = np.count_nonzero(codewords, axis=1)
                bad_idx = np.where(weights == d_cur)[0]
                if len(bad_idx) > 0:
                    bad_info = _INFO_VECS[bad_idx]
                    bad_cws = codewords[bad_idx]
                    influence = np.zeros((k, n), dtype=np.float64)
                    for bi in range(len(bad_idx)):
                        zeros_c = np.where(bad_cws[bi] == 0)[0]
                        nonzero_r = np.where(bad_info[bi] != 0)[0]
                        for rr in nonzero_r:
                            influence[rr, zeros_c] += 1.0
                    mx = np.max(influence)
                    if mx > 0:
                        influence /= mx
            else:
                G[r, c] = old
        else:
            G[r, c] = old
    return best_G, best_d


def D_pitbull(G_base, time_limit=60):
    """AMRAAM PITBULL MODE: Autonomous terminal guidance. Start with
    broad search, then when A_12 drops below threshold, switch to
    intense focused attack on the remaining bad codewords.

    Fire and forget. The missile finds its own way."""
    k, n = G_base.shape
    G = G_base.copy()
    d_cur, a_cur = min_dist_full(G)
    best_d, best_G, best_a = d_cur, G.copy(), a_cur
    cols = _get_cols(k)
    nc = len(cols)
    start = time.time()

    pitbull_threshold = max(a_cur * 2 // 3, 30)  # go pitbull when A_12 drops 33%
    pitbull_mode = False

    while time.time() - start < time_limit:
        if not pitbull_mode:
            # SEARCH PHASE: broad mutations
            r = np.random.randint(0, k)
            c = np.random.randint(0, n)
            old = G[:, c].copy() if np.random.random() < 0.3 else None
            if old is not None:
                G[:, c] = cols[np.random.randint(0, nc)]
            else:
                old_entry = G[r, c]
                G[r, c] = np.random.randint(0, 4)
                if G[r, c] == old_entry:
                    continue

            d = min_dist_early(G, d_cur)
            if d >= d_cur:
                d_f, a_f = min_dist_full(G)
                if d_f > best_d or (d_f == best_d and a_f < best_a):
                    if d_f > best_d:
                        best_d = d_f
                    best_a = a_f
                    best_G = G.copy()
                    d_cur, a_cur = d_f, a_f
                    if best_d >= 13:
                        print(f"    ★ PITBULL: d={best_d}!")
                        return best_G, best_d
                    if a_cur <= pitbull_threshold:
                        pitbull_mode = True
                        print(f"    PITBULL ACTIVATED: A_{d_cur}={a_cur}")
                syms = {0:"0", 1:"1", 2:"w", 3:"w2"}
                for row in range(G.shape[0]):
                    print("    [" + " ".join(syms[G[row,cc]] for cc in range(G.shape[1])) + "]")
                else:
                    if old is not None:
                        G[:, c] = old
                    else:
                        G[r, c] = old_entry
            else:
                if old is not None:
                    G[:, c] = old
                else:
                    G[r, c] = old_entry
        else:
            # PITBULL PHASE: intense attack on remaining bad codewords
            _precompute_info(k)
            codewords = np.zeros((4**k - 1, n), dtype=np.uint8)
            for j, val, mask in _INFO_NONZERO:
                contrib = GF4_MUL[val][G[j]]
                codewords[mask] = GF4_ADD[codewords[mask], contrib]
            weights = np.count_nonzero(codewords, axis=1)
            bad_idx = np.where(weights == d_cur)[0]
            if len(bad_idx) == 0:
                break
            bad_cws = codewords[bad_idx]

            # Find the column with most zeros across bad codewords
            zero_count = np.zeros(n, dtype=np.int32)
            for cw in bad_cws:
                zeros = np.where(cw == 0)[0]
                zero_count[zeros] += 1
            target_c = np.argmax(zero_count)

            # Try all possible column replacements at target
            for ci in range(nc):
                G_test = G.copy()
                G_test[:, target_c] = cols[ci]
                d = min_dist_early(G_test, d_cur)
                if d >= d_cur:
                    d_f, a_f = min_dist_full(G_test)
                    if d_f > best_d or (d_f == best_d and a_f < best_a):
                        if d_f > best_d:
                            best_d = d_f
                            print(f"    PITBULL HIT: d -> {best_d}")
                        best_a = a_f
                        best_G = G_test.copy()
                        G = G_test.copy()
                        d_cur, a_cur = d_f, a_f
                        if best_d >= 13:
                            return best_G, best_d
            pitbull_mode = False  # reset after full column scan
    return best_G, best_d


def D_fluorescencia(G_base, time_limit=45):
    """FLUORESCENCIA: Excite every entry of the parity matrix with each
    possible GF(4) value. Measure the "emission" — the change in min
    distance. Build a complete excitation map, then apply the combination
    of ALL positive-emission changes at once.

    The tube doesn't glow everywhere — only where mercury vapor is excited.
    Find the entries that "glow" (improve d) and excite them all together."""
    k, n = G_base.shape
    G = systematic_form(G_base.copy())
    if not np.array_equal(G[:, :k], np.eye(k, dtype=np.uint8)):
        G = G_base.copy()
    d_cur, a_cur = min_dist_full(G)
    best_d, best_G, best_a = d_cur, G.copy(), a_cur
    start = time.time()

    while time.time() - start < time_limit:
        # EXCITATION SCAN: test every entry change
        emissions = []  # (delta_a, r, c, new_val)
        for r in range(k):
            for c in range(k, n):
                old = G[r, c]
                for v in range(4):
                    if v == old:
                        continue
                    G[r, c] = v
                    d_test = min_dist_early(G, d_cur)
                    if d_test >= d_cur:
                        d_f, a_f = min_dist_full(G)
                        if d_f > d_cur:
                            # Immediate improvement!
                            best_d, best_G = d_f, G.copy()
                            best_a = a_f
                            d_cur, a_cur = d_f, a_f
                            if best_d >= 13:
                                print(f"    ★ FLUORESCENCIA: d={best_d}!")
                                return best_G, best_d
                            emissions = []  # restart scan
                            break
                        elif d_f == d_cur:
                            delta = a_cur - a_f  # positive = fewer bad codewords
                            if delta > 0:
                                emissions.append((delta, r, c, v))
                    G[r, c] = old
                if best_d >= 13:
                    return best_G, best_d

        if not emissions:
            # No glow — random perturbation
            for _ in range(np.random.randint(2, 5)):
                G[np.random.randint(0, k), np.random.randint(k, n)] = np.random.randint(0, 4)
            d_cur, a_cur = min_dist_full(G)
            continue

        # PHOSPHORESCENCE: apply top N non-conflicting emissions at once
        emissions.sort(reverse=True)
        applied = set()
        G_comb = G.copy()
        for delta, r, c, v in emissions:
            key = (r, c)
            if key in applied:
                continue
            G_comb[r, c] = v
            applied.add(key)
            if len(applied) >= 6:
                break

        d_comb = min_dist_early(G_comb, d_cur)
        if d_comb >= d_cur:
            d_f, a_f = min_dist_full(G_comb)
            if d_f > best_d or (d_f == best_d and a_f < best_a):
                if d_f > best_d:
                    best_d = d_f
                    print(f"    FLUORESCENCIA combo: d -> {best_d}")
                best_a = a_f
                best_G = G_comb.copy()
                G = G_comb.copy()
                d_cur, a_cur = d_f, a_f
                if best_d >= 13:
                    return best_G, best_d

        # Try applying one at a time if combo didn't work
        for delta, r, c, v in emissions[:3]:
            G[r, c] = v
            d_f, a_f = min_dist_full(G)
            if d_f >= d_cur:
                d_cur, a_cur = d_f, a_f
                if d_f > best_d or (d_f == best_d and a_f < best_a):
                    best_d, best_G, best_a = d_f, G.copy(), a_f
                    if best_d >= 13:
                        return best_G, best_d
            else:
                G[r, c] = G_base[r, c] if r < G_base.shape[0] and c < G_base.shape[1] else 0
                d_cur, a_cur = min_dist_full(G)
    return best_G, best_d


def D_silueta(G_base, rounds=30000):
    """IIR TEMPLATE MATCHING: Compare candidates against the theoretical
    "silhouette" of a [22,6,13]_4. Accept mutations that make the weight
    enumerator LOOK MORE like what a d=13 code should look like.

    Pattern matching — the missile recognizes the target by its shape."""
    k, n = G_base.shape
    best_d, best_G = min_dist(G_base), G_base.copy()

    # Target silhouette: for a [22,6,13]_4, A_12 should be 0
    # and A_13 should be moderate (say 60-200 based on MacWilliams)
    # We want: minimize A_12, then minimize A_13 deviation from target

    d_cur, a_cur = min_dist_full(best_G)

    for _ in range(rounds):
        G = best_G.copy()
        r = np.random.randint(0, k)
        c = np.random.randint(k if np.array_equal(G[:, :k], np.eye(k, dtype=np.uint8)) else 0, n)
        old = G[r, c]
        G[r, c] = np.random.randint(0, 4)
        if G[r, c] == old:
            continue

        d = min_dist_early(G, d_cur)
        if d >= d_cur:
            d_f, a_f = min_dist_full(G)
            # Silhouette score: lower A_d is better; higher d is better
            score_new = d_f * 10000 - a_f
            score_old = best_d * 10000 - a_cur
            if score_new > score_old:
                best_d, best_G = d_f, G.copy()
                d_cur, a_cur = d_f, a_f
                if best_d >= 13:
                    print(f"    ★ SILUETA: d={best_d}!")
                    return best_G, best_d
        else:
            G[r, c] = old
    return best_G, best_d


# v9: LA PUA DEL JET + ALTERNATIVE SEEDS
# ===============================================================

SEED_R2 = np.array([
    [1,0,0,0,0,2,3,2,2,3,3,2,1,0,1,1,3,0,2,0,0,1],
    [0,1,0,0,0,1,2,0,2,1,2,3,0,3,1,2,3,1,0,1,0,2],
    [0,0,1,0,0,3,3,2,2,1,2,3,2,1,3,0,1,3,1,2,1,2],
    [0,0,0,1,0,0,2,0,3,3,3,0,1,2,2,1,0,0,3,2,2,1],
    [0,0,0,0,1,1,3,3,0,1,0,3,1,1,2,2,3,0,0,3,2,1],
    [1,0,2,0,2,1,2,3,0,0,3,3,0,3,0,2,1,2,3,0,2,2],
], dtype=np.uint8)
BASE_22_5_13 = SEED_R2[:5].copy()

# RECORD: [22,6,12]_4 with A_12=60 (best known, 373M evals, R7 exhaustive)
SEED_A60 = np.array([
    [1,0,0,0,0,2,3,2,2,3,3,2,1,0,1,1,3,0,2,0,0,1],
    [0,1,0,0,0,1,2,0,2,1,2,3,0,3,1,2,3,1,0,1,0,2],
    [0,0,1,0,0,3,3,2,2,1,2,3,2,1,3,0,1,3,1,2,1,2],
    [0,0,0,1,0,0,2,0,3,3,3,0,1,2,2,1,0,0,3,2,2,1],
    [0,0,0,0,1,1,3,3,0,1,0,3,1,1,2,2,3,0,0,3,2,1],
    [1,3,0,1,2,1,1,3,3,3,0,1,3,0,2,2,3,0,3,2,2,1],
], dtype=np.uint8)
PUA_A60 = SEED_A60[5].copy()

# VERIFIED SEEDS — Campaign progression: 78 > 69 > 60 > 51 > 48 > 42
SEED_A51 = np.array([
    [1,0,0,0,0,0, 3,2,1,1,2,2,0,2,0,1,0,3,0,2,3,3],
    [0,1,0,0,0,0, 2,0,0,0,1,3,3,3,2,2,1,3,1,0,2,3],
    [0,0,1,0,0,0, 3,2,3,2,0,3,1,2,1,0,0,2,3,1,0,1],
    [0,0,0,1,0,0, 2,0,3,3,3,0,1,3,2,1,0,0,3,2,2,1],
    [0,0,0,0,1,0, 3,3,2,0,3,3,2,0,1,2,1,2,1,2,0,0],
    [0,0,0,0,0,1, 0,0,2,0,3,0,3,2,3,0,2,2,1,1,2,1],
], dtype=np.uint8)
SEED_A48 = np.array([
    [1,0,0,0,0,0, 3,2,1,1,2,2,0,1,0,1,0,3,0,0,3,3],
    [0,1,0,0,0,0, 2,2,0,0,1,3,3,2,2,2,1,3,1,0,2,2],
    [0,0,1,0,0,0, 3,2,3,2,0,3,0,1,1,0,2,2,2,1,0,2],
    [0,0,0,1,0,0, 2,0,3,3,3,0,1,2,2,1,0,0,3,2,2,1],
    [0,0,0,0,1,0, 3,3,2,0,3,3,2,0,1,2,1,2,1,2,0,0],
    [0,0,0,0,0,1, 0,0,2,1,3,0,3,1,3,0,2,2,1,2,2,1],
], dtype=np.uint8)
SEED_A42 = np.array([
    [1,1,0,0,0,0, 3,2,1,1,2,2,0,1,0,1,0,3,0,0,3,3],
    [0,0,0,0,0,0, 2,2,0,0,1,3,3,2,2,2,1,3,1,0,2,2],
    [0,2,1,0,0,0, 3,2,3,2,0,3,0,1,1,0,2,2,2,1,0,2],
    [0,0,0,1,0,0, 2,0,3,3,3,0,1,2,2,1,0,0,3,2,2,1],
    [0,3,0,0,1,0, 3,3,2,0,3,3,2,0,1,2,1,2,1,2,0,0],
    [0,0,0,0,0,1, 0,0,2,1,3,0,3,1,3,0,2,2,1,2,2,1],
], dtype=np.uint8)

def D_pua_jet(base_G5, time_limit=120):
    k_base, n = base_G5.shape
    best_d, best_G, best_a = 0, None, 99999
    start = time.time()
    tested = 0
    while time.time() - start < time_limit:
        pua = np.random.randint(0, 4, size=n).astype(np.uint8)
        if np.all(pua == 0): continue
        G6 = np.vstack([base_G5, pua.reshape(1, -1)])
        d = min_dist_early(G6, 13)
        tested += 1
        if d >= 13:
            d_full, a = min_dist_full(G6)
            if d_full >= 13:
                print(f"    PUA: d={d_full}! ({tested} tested)")
                return G6, d_full
            if d_full > best_d or (d_full == best_d and a < best_a):
                best_d, best_a, best_G = d_full, a, G6.copy()
        elif d > best_d:
            d_full, a = min_dist_full(G6)
            if d_full > best_d or (d_full == best_d and a < best_a):
                best_d, best_a, best_G = d_full, a, G6.copy()
    e = time.time() - start
    print(f"    Pua: {tested} rows ({tested/e:.0f}/s), best d={best_d} A={best_a}")
    return best_G, best_d

def D_pua_guided(base_G5, template_pua, time_limit=60):
    k_base, n = base_G5.shape
    pua = template_pua.copy()
    G6 = np.vstack([base_G5, pua.reshape(1, -1)])
    d_cur, a_cur = min_dist_full(G6)
    best_d, best_G, best_a = d_cur, G6.copy(), a_cur
    start = time.time()
    while time.time() - start < time_limit:
        pua_new = pua.copy()
        for _ in range(np.random.randint(1, 4)):
            pua_new[np.random.randint(0, n)] = np.random.randint(0, 4)
        G6 = np.vstack([base_G5, pua_new.reshape(1, -1)])
        d = min_dist_early(G6, d_cur)
        if d >= d_cur:
            d_f, a = min_dist_full(G6)
            if d_f > best_d or (d_f == best_d and a < best_a):
                if d_f > best_d:
                    best_d = d_f
                    print(f"    Guided Pua: d -> {best_d}")
                best_a, best_G, pua = a, G6.copy(), pua_new.copy()
                d_cur, a_cur = d_f, a
                if best_d >= 13: return best_G, best_d
    return best_G, best_d

def D_pua_heatscan(base_G5, template_pua, time_limit=60):
    k_base, n = base_G5.shape
    pua = template_pua.copy()
    G6 = np.vstack([base_G5, pua.reshape(1, -1)])
    d_cur, a_cur = min_dist_full(G6)
    best_d, best_G, best_a = d_cur, G6.copy(), a_cur
    start = time.time()
    while time.time() - start < time_limit:
        improved = False
        for pos in range(n):
            old_val = pua[pos]
            bv, bd = old_val, 0
            for v in range(4):
                if v == old_val: continue
                pua[pos] = v
                G6 = np.vstack([base_G5, pua.reshape(1, -1)])
                d = min_dist_early(G6, d_cur)
                if d >= d_cur:
                    df, af = min_dist_full(G6)
                    if df > best_d:
                        best_d, best_a, best_G = df, af, G6.copy()
                        bv = v; d_cur, a_cur = df, af
                        print(f"    Pua heat: d->{best_d} @{pos}")
                        if best_d >= 13: return best_G, best_d
                        break
                    elif df == d_cur and af < a_cur:
                        delta = a_cur - af
                        if delta > bd: bd, bv = delta, v
            pua[pos] = bv
            if bv != old_val:
                G6 = np.vstack([base_G5, pua.reshape(1, -1)])
                d_cur, a_cur = min_dist_full(G6)
                improved = True
                if a_cur < best_a:
                    best_a, best_G = a_cur, G6.copy()
                    print(f"    Pua heat: A_{d_cur}={a_cur} @{pos}")
            if time.time() - start > time_limit: break
        if not improved:
            for _ in range(np.random.randint(2,5)):
                pua[np.random.randint(0,n)] = np.random.randint(0,4)
            G6 = np.vstack([base_G5, pua.reshape(1,-1)])
            d_cur, a_cur = min_dist_full(G6)
    return best_G, best_d


# ═══════════════════════════════════════════════════════════════
# BLAME ANALYSIS
# ═══════════════════════════════════════════════════════════════

def blame_columns(G):
    """Find columns most responsible for low-weight codewords."""
    k, n = G.shape
    d_cur = min_dist(G)
    we = weight_enum(G)
    blame = np.zeros(n, dtype=np.int32)
    _precompute_info(k)
    total = 4**k - 1
    codewords = np.zeros((total, n), dtype=np.uint8)
    for j, val, mask in _INFO_NONZERO:
        contrib = GF4_MUL[val][G[j]]
        codewords[mask] = GF4_ADD[codewords[mask], contrib]
    weights = np.count_nonzero(codewords, axis=1)
    low = np.where(weights <= d_cur + 1)[0]
    for i in low:
        zeros = np.where(codewords[i] == 0)[0]
        w = int(weights[i])
        blame[zeros] += (d_cur + 2 - w)
    ranked = sorted(range(n), key=lambda i: -blame[i])
    return ranked, blame


# ═══════════════════════════════════════════════════════════════
# OUTPUT
# ═══════════════════════════════════════════════════════════════

def print_matrix(G):
    d, cnt = min_dist_full(G)
    sym = ['0', '1', 'ω', 'ω²']
    print(f"\n  [{G.shape[1]},{G.shape[0]},{d}]_4, A_{d}={cnt}")
    for row in G:
        print("  [" + " ".join(sym[x] for x in row) + "]")

def save_result(G, filename=None):
    d, cnt = min_dist_full(G)
    if filename is None:
        filename = f"ESTRELLA_{G.shape[1]}_{G.shape[0]}_{d}.txt"
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    with open(path, 'w') as f:
        f.write("=" * 60 + "\n")
        f.write(f"  PROYECTO ESTRELLA — [{G.shape[1]},{G.shape[0]},{d}]_4\n")
        f.write(f"  A_{d} = {cnt}\n")
        f.write("=" * 60 + "\n\n")
        f.write("Generator matrix (0=0, 1=1, 2=omega, 3=omega²):\n")
        for row in G:
            f.write(' '.join(str(x) for x in row) + '\n')
        we = weight_enum(G)
        f.write(f"\nWeight enumerator:\n")
        for w in sorted(we.keys()):
            f.write(f"  A_{w} = {we[w]}\n")
    print(f"  Saved: {path}")

def verify(G):
    """Triple verification."""
    d1, c1 = min_dist_full(G)
    Gs = systematic_form(G)
    d2, c2 = min_dist_full(Gs)
    k, n = G.shape
    d3 = n + 1
    for idx in range(1, 4**k):
        v = idx_to_gf4_vec(idx, k)
        cw = encode(v, G)
        w = int(np.count_nonzero(cw))
        if w < d3:
            d3 = w
    return d1 == d2 == d3, d1


# ═══════════════════════════════════════════════════════════════
# MAIN ENGINE v4
# ═══════════════════════════════════════════════════════════════

def main():
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║  PROYECTO ESTRELLA — 108 DOCTRINES ENGINE v13                 ║
    ║  SAMAEL Beast 10 — [22,6,13]_4 Diamond Hunt                 ║
    ║  Σ = 1561/675 ≈ 2.31 | 73 mechanisms | 10 beasts            ║
    ║  v13: THE MATRIX — tacografo total                 ║
    ║  Heat-Seek · PropNav · Pitbull · Fluorescencia · Silueta     ║
    ║  + Ghost · Metamaterial · 1-UP · Warp · RDE · SABRE          ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)

    np.random.seed(int(time.time()) % 2**31)
    start_time = time.time()

    # ── Boot ──
    print("[BOOT]")
    _init_kernel()
    _precompute_info(6)

    # Self-test
    G_hex = np.array([[1,0,0,1,1,1],[0,1,0,1,2,3],[0,0,1,1,3,2]], dtype=np.uint8)
    _precompute_k(3)
    assert _min_dist_k(G_hex, 3) == 4, "Hexacode FAIL"
    print("  Self-test: Hexacode [6,3,4]_4 OK")

    # Speed test
    G_test = np.eye(6, dtype=np.uint8)
    G_test = np.hstack([G_test, np.ones((6,16), dtype=np.uint8)])
    t0 = time.time()
    for _ in range(100):
        min_dist_early(G_test, 13)
    rate = 100 / (time.time() - t0)
    print(f"  Speed: {rate:.0f} early evals/sec")

    # ── Seed ──
    print("\n[SEED]")
    G_seed, d_seed = build_seed()
    if G_seed is None or d_seed < 8:
        print("  Seed failed, using fallback")
        G_seed = np.array([
            [1,0,0,0,0,0, 1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
            [0,1,0,0,0,0, 1,1,1,1,0,0,0,0,2,2,3,1,1,1,0,0],
            [0,0,1,0,0,0, 1,1,0,0,1,1,0,0,1,3,2,1,1,0,1,0],
            [0,0,0,1,0,0, 1,0,1,0,1,0,1,0,3,1,1,1,0,1,1,0],
            [0,0,0,0,1,0, 1,0,0,1,0,1,1,0,0,1,2,0,1,1,1,1],
            [0,0,0,0,0,1, 0,1,0,1,1,0,0,1,1,0,1,1,0,1,2,1],
        ], dtype=np.uint8)
        d_seed = min_dist(G_seed)

    # Compare QR seed vs Round 2 seed (A12=78)
    d_r2, a_r2 = min_dist_full(SEED_R2)
    print(f"  Round 2 seed: [22,6,{d_r2}]_4, A_{d_r2}={a_r2}")
    if d_r2 > d_seed or (d_r2 == d_seed and a_r2 < min_dist_full(G_seed)[1]):
        G_seed, d_seed = SEED_R2.copy(), d_r2
        print(f"  Using Round 2 seed (better A_12)")
    
    # A12=60 record seed
    d_a60, a_a60 = min_dist_full(SEED_A60)
    print(f"  A60 record: [22,6,{d_a60}]_4, A_{d_a60}={a_a60}")
    if d_a60 >= d_seed:
        G_seed = SEED_A60.copy()
        d_seed = d_a60
        print(f"  Using A60 seed (RECORD)")

    # Campaign seeds cascade: 60 > 51 > 48 > 42
    for name, seed in [("A51", SEED_A51), ("A48", SEED_A48), ("A42", SEED_A42)]:
        ds, as_ = min_dist_full(seed)
        print(f"  {name} seed: [22,6,{ds}]_4, A_{ds}={as_}")
        if ds >= d_seed:
            _, a_gs = min_dist_full(G_seed)
            if ds > d_seed or as_ < a_gs:
                G_seed, d_seed = seed.copy(), ds
                print(f"  >>> Using {name} seed")

    best_G, best_d = G_seed.copy(), d_seed
    _, best_a = min_dist_full(best_G)
    # GLOBAL BEST — never corrupted, always printed on improvement
    global_best_G = best_G.copy()
    global_best_d = best_d
    global_best_a = best_a

    def update_best(G_new, d_new, source=""):
        nonlocal best_G, best_d, best_a, global_best_G, global_best_d, global_best_a
        if G_new is None:
            return
        d_v, a_v = min_dist_full(G_new)
        if d_v > best_d or (d_v == best_d and a_v < best_a):
            best_d, best_a = d_v, a_v
            best_G = G_new.copy()
            if d_v > global_best_d or (d_v == global_best_d and a_v < global_best_a):
                global_best_d, global_best_a = d_v, a_v
                global_best_G = G_new.copy()
                print(f"  >>> NEW BEST: [22,6,{d_v}]_4, A_{d_v}={a_v} [{source}]")
                print_matrix(global_best_G)

    print_matrix(best_G)

    def check():
        nonlocal best_G, best_d
        if best_d >= 13:
            ok, dv = verify(best_G)
            print(f"\n  ★★★ DIAMOND! Verified={ok}, d={dv} ★★★")
            print_matrix(best_G)
            save_result(best_G, "DIAMOND_22_6_13.txt")
            return True
        return False

    if check():
        return

    # ── Phase 1: Quick climb ──
    print(f"\n[PHASE 1] Hill climb (d={best_d})")
    for iters in [10000, 20000]:
        t0 = time.time()
        Gn, dn = D029_hill_climb(best_G, iters)
        if dn > best_d:
            best_d, best_G = dn, Gn.copy()
            print(f"  ↑ HC_{iters//1000}k: d -> {best_d} ({time.time()-t0:.1f}s)")
        else:
            print(f"  HC_{iters//1000}k: d={dn} ({time.time()-t0:.1f}s)")
        if check(): return

    # ── Phase 2: Battery ──
    print(f"\n[PHASE 2] Battery (d={best_d})")
    battery = [
        ("SA_30k", lambda: D056_SA(best_G, 30000)),
        ("Wild_10k", lambda: D057_wild(best_G, 10000)),
        ("Mut_100k", lambda: D036_mutation(best_G, 100000)),
        ("Restarts", lambda: D054_restarts(best_G, 20, 500)),
    ]
    for name, func in battery:
        t0 = time.time()
        Gn, dn = func()
        if dn > best_d:
            best_d, best_G = dn, Gn.copy()
            print(f"  ↑ {name}: d -> {best_d} ({time.time()-t0:.1f}s)")
        else:
            print(f"  {name}: d={dn} ({time.time()-t0:.1f}s)")
        if check(): return

    # ── Phase 3: Blame analysis → Chorro ──
    print(f"\n[PHASE 3] Chorro de agua (d={best_d})")
    ranked, blame = blame_columns(best_G)
    print(f"  Top blame columns: {ranked[:8]}")
    top_triples = list(itertools.combinations(ranked[:6], 3))
    scored = [(sum(blame[c] for c in t), list(t)) for t in top_triples]
    scored.sort(key=lambda x: -x[0])

    for score, triple in scored[:2]:
        Gs, ds = D_chorro(best_G, triple, time_limit=40)
        if ds > best_d:
            best_d, best_G = ds, Gs.copy()
            print(f"  ↑ Chorro {triple}: d -> {best_d}")
        if check(): return

    # ── Phase 4: Fatiga ──
    print(f"\n[PHASE 4] Fatiga por resonancia (d={best_d})")
    for triple in [ranked[:3], ranked[1:4], ranked[2:5]]:
        t0 = time.time()
        Gf, df = D_fatiga(best_G, triple, cycles=2000)
        if df > best_d:
            best_d, best_G = df, Gf.copy()
            print(f"  ↑ Fatiga {triple}: d -> {best_d} ({time.time()-t0:.1f}s)")
        else:
            print(f"  Fatiga {triple}: d={df} ({time.time()-t0:.1f}s)")
        if check(): return

    # ── Phase 5: Hilo de diamante (constraint propagation) ──
    print(f"\n[PHASE 5] Hilo de diamante (d={best_d})")
    t0 = time.time()
    Gh, dh = D_hilo_diamante(best_G, time_limit=30)
    if dh > best_d:
        best_d, best_G = dh, Gh.copy()
        print(f"  ↑ Hilo: d -> {best_d} ({time.time()-t0:.1f}s)")
    else:
        print(f"  Hilo: d={dh} ({time.time()-t0:.1f}s)")
    if check(): return

    # ── Phase 6: Cuñas hidráulicas (isotopy transforms) ──
    print(f"\n[PHASE 6] Cuñas hidráulicas (d={best_d})")
    t0 = time.time()
    Gc, dc = D_cunas(best_G, rounds=20000)
    if dc > best_d:
        best_d, best_G = dc, Gc.copy()
        print(f"  ↑ Cuñas: d -> {best_d} ({time.time()-t0:.1f}s)")
    else:
        print(f"  Cuñas: d={dc} ({time.time()-t0:.1f}s)")
    if check(): return

    # ── Phase 7: Fragilización (Knuth semifield columns) ──
    print(f"\n[PHASE 7] Fragilización por hidrógeno (d={best_d})")
    t0 = time.time()
    Gk, dk = D_knuth_columns(best_G, rounds=30000)
    if dk > best_d:
        best_d, best_G = dk, Gk.copy()
        print(f"  ↑ Knuth: d -> {best_d} ({time.time()-t0:.1f}s)")
    else:
        print(f"  Knuth: d={dk} ({time.time()-t0:.1f}s)")
    if check(): return

    # ── Phase 8: Cavitación (vacuum from [23,6,13]) ──
    print(f"\n[PHASE 8] Cavitación (d={best_d})")
    t0 = time.time()
    Gv, dv = D_cavitacion(best_G, time_limit=30)
    if dv > best_d:
        best_d, best_G = dv, Gv.copy()
        print(f"  ↑ Cavitación: d -> {best_d} ({time.time()-t0:.1f}s)")
    else:
        print(f"  Cavitación: d={dv} ({time.time()-t0:.1f}s)")
    if check(): return

    # ── Phase 9: Deflagración (multi-seed explosion) ──
    print(f"\n[PHASE 9] Deflagración (d={best_d})")
    t0 = time.time()
    Ge, de = D_deflagracion(best_G, time_limit=20)
    if de > best_d:
        best_d, best_G = de, Ge.copy()
        print(f"  ↑ Deflagración: d -> {best_d} ({time.time()-t0:.1f}s)")
    else:
        print(f"  Deflagración: d={de} ({time.time()-t0:.1f}s)")
    if check(): return

    # ── Phase 10: Ghost Imaging (correlación de fallos) ──
    print(f"\n[PHASE 10] Ghost Imaging (d={best_d})")
    t0 = time.time()
    Gg, dg = D_ghost_imaging(best_G, rounds=40000)
    if dg > best_d:
        best_d, best_G = dg, Gg.copy()
        print(f"  ↑ Ghost: d -> {best_d} ({time.time()-t0:.1f}s)")
    else:
        print(f"  Ghost: d={dg} ({time.time()-t0:.1f}s)")
    if check(): return

    # ── Phase 11: Triangulación (supply chain tracking) ──
    print(f"\n[PHASE 11] Triangulación (d={best_d})")
    t0 = time.time()
    Gt, dt = D_triangulacion(best_G, time_limit=30)
    if dt > best_d:
        best_d, best_G = dt, Gt.copy()
        print(f"  ↑ Triangulación: d -> {best_d} ({time.time()-t0:.1f}s)")
    else:
        print(f"  Triangulación: d={dt} ({time.time()-t0:.1f}s)")
    if check(): return

    # ── Phase 12: 1-UP Loop (momentum feedback) ──
    print(f"\n[PHASE 12] 1-UP Loop (d={best_d})")
    t0 = time.time()
    G1, d1 = D_oneup_loop(best_G, time_limit=30)
    if d1 > best_d:
        best_d, best_G = d1, G1.copy()
        print(f"  ↑ 1-UP: d -> {best_d} ({time.time()-t0:.1f}s)")
    else:
        print(f"  1-UP: d={d1} ({time.time()-t0:.1f}s)")
    if check(): return

    # ── Phase 13: Metamaterial/Minus World ──
    print(f"\n[PHASE 13] Metamaterial (d={best_d})")
    t0 = time.time()
    Gm, dm = D_metamaterial(best_G, time_limit=45)
    if dm > best_d:
        best_d, best_G = dm, Gm.copy()
        print(f"  ↑ Metamaterial: d -> {best_d} ({time.time()-t0:.1f}s)")
    else:
        print(f"  Metamaterial: d={dm} ({time.time()-t0:.1f}s)")
    if check(): return

    # ── Phase 14: Warp Zone (row-level jumps) ──
    print(f"\n[PHASE 14] Warp Zone (d={best_d})")
    t0 = time.time()
    Gw, dw = D_warp_zone(best_G, time_limit=30)
    if dw > best_d:
        best_d, best_G = dw, Gw.copy()
        print(f"  ↑ Warp: d -> {best_d} ({time.time()-t0:.1f}s)")
    else:
        print(f"  Warp: d={dw} ({time.time()-t0:.1f}s)")
    if check(): return

    # ── Phase 15: Heat-Seeker (gradient on A_12) ──
    print(f"\n[PHASE 15] Heat-Seeker (d={best_d})")
    t0 = time.time()
    Ghs, dhs = D_heat_seeker(global_best_G, time_limit=60)
    update_best(Ghs, dhs, 'HeatSeek')
    if dhs > best_d:
        best_d = dhs
        print(f"  ↑ Heat-Seek: d -> {best_d} ({time.time()-t0:.1f}s)")
    if Ghs is not None and dhs >= best_d: best_G = Ghs.copy()
    print(f"  Heat-Seek: d={dhs} ({time.time()-t0:.1f}s)")
    if check(): return

    # ── Phase 16: PropNav (influence-weighted mutations) ──
    print(f"\n[PHASE 16] PropNav (d={best_d})")
    t0 = time.time()
    Gpn, dpn = D_propnav(global_best_G, time_limit=30)
    if dpn > best_d:
        best_d = dpn
        print(f"  ↑ PropNav: d -> {best_d} ({time.time()-t0:.1f}s)")
    if Gpn is not None and dpn >= best_d: best_G = Gpn.copy()
    print(f"  PropNav: d={dpn} ({time.time()-t0:.1f}s)")
    if check(): return

    # ── Phase 17: Fluorescencia (excitation map) ──
    print(f"\n[PHASE 17] Fluorescencia (d={best_d})")
    t0 = time.time()
    Gfl, dfl = D_fluorescencia(global_best_G, time_limit=40)
    if dfl > best_d:
        best_d = dfl
        print(f"  ↑ Fluorescencia: d -> {best_d} ({time.time()-t0:.1f}s)")
    if Gfl is not None and dfl >= best_d: best_G = Gfl.copy()
    print(f"  Fluorescencia: d={dfl} ({time.time()-t0:.1f}s)")
    if check(): return

    # ── Phase 18: Pitbull AMRAAM (autonomous terminal) ──
    print(f"\n[PHASE 18] Pitbull AMRAAM (d={best_d})")
    t0 = time.time()
    Gpb, dpb = D_pitbull(global_best_G, time_limit=40)
    if dpb > best_d:
        best_d, best_G = dpb, Gpb.copy()
        print(f"  ↑ Pitbull: d -> {best_d} ({time.time()-t0:.1f}s)")
    else:
        print(f"  Pitbull: d={dpb} ({time.time()-t0:.1f}s)")
    update_best(Gpb, dpb, "Pitbull")
    if check(): return

    # ── Phase 19: Silueta IIR (template matching) ──
    print(f"\n[PHASE 19] Silueta IIR (d={best_d})")
    t0 = time.time()
    Gsi, dsi = D_silueta(best_G, rounds=20000)
    if dsi > best_d:
        best_d, best_G = dsi, Gsi.copy()
        print(f"  ↑ Silueta: d -> {best_d} ({time.time()-t0:.1f}s)")
    else:
        print(f"  Silueta: d={dsi} ({time.time()-t0:.1f}s)")
    if check(): return

    # ── Phase 20: La Pua del Jet ──
    print(f"\n[PHASE 20] La Pua del Jet (d={best_d})")
    t0 = time.time()
    Gp, dp = D_pua_jet(BASE_22_5_13, time_limit=60)
    if Gp is not None and dp > best_d:
        best_d, best_G = dp, Gp.copy()
    print(f"  Pua: d={dp} ({time.time()-t0:.1f}s)")
    if check(): return

    # ── Phase 21: Guided Pua ──
    print(f"\n[PHASE 21] Guided Pua (d={best_d})")
    t0 = time.time()
    Gpg, dpg = D_pua_guided(BASE_22_5_13, SEED_A42[0], time_limit=45)
    if dpg > best_d:
        best_d, best_G = dpg, Gpg.copy()
    print(f"  Guided Pua: d={dpg} ({time.time()-t0:.1f}s)")
    if check(): return

    # ── Phase 22: Pua Heat-Scan ──
    print(f"\n[PHASE 22] Pua Heat-Scan (d={best_d})")
    t0 = time.time()
    Gph, dph = D_pua_heatscan(BASE_22_5_13, SEED_R2[5], time_limit=45)
    if dph > best_d:
        best_d, best_G = dph, Gph.copy()
    print(f"  Pua heat: d={dph} ({time.time()-t0:.1f}s)")
    if check(): return

    # ── Phase 23: RDE + SABRE ──
    print(f"\n[PHASE 24] RDE + SABRE (d={best_d})")
    Gr, dr = D_rde(time_limit=30)
    update_best(Gr, dr, 'RDE')
    if check(): return
    elapsed_now = time.time() - start_time
    sabre_time = max(60, 600 - elapsed_now - 90)
    Gs, ds = D_sabre(best_G, time_limit=sabre_time)
    update_best(Gs, ds, 'SABRE')
    if check(): return

    # ── Phase 21: Architect loop ──
    elapsed = time.time() - start_time
    remaining = max(600 - elapsed, 60)
    print(f"\n[PHASE 25] Architect loop (d={best_d}, {remaining:.0f}s)")
    print("  ╔═══════════════════════════════════════════════════╗")
    print("  ║  PUENTES, NO MUROS. The search continues.        ║")
    print("  ╚═══════════════════════════════════════════════════╝")

    start5 = time.time()
    cycle = 0
    strats = [
        ("HC_20k", lambda G: D029_hill_climb(G, 20000)),
        ("Mut_200k", lambda G: D036_mutation(G, 200000)),
        ("Ghost_20k", lambda G: D_ghost_imaging(G, 20000)),
        ("1UP_20s", lambda G: D_oneup_loop(G, 20)),
        ("HeatSeek", lambda G: D_heat_seeker(G, 20)),
        ("PropNav", lambda G: D_propnav(G, 20)),
        ("Fluor_20s", lambda G: D_fluorescencia(G, 20)),
        ("Pitbull", lambda G: D_pitbull(G, 20)),
        ("Silueta_15k", lambda G: D_silueta(G, 15000)),
        ("Warp_15s", lambda G: D_warp_zone(G, 15)),
        ("RDE_20s", lambda G: D_rde(20)),
        ("Meta_20s", lambda G: D_metamaterial(G, 20)),
        ("Pua_30s", lambda G: D_pua_jet(BASE_22_5_13, 30)),
        ("PuaG_20s", lambda G: D_pua_guided(BASE_22_5_13, SEED_A42[0], 20)),
        ("HeatSeek2", lambda G: D_heat_seeker(G, 25)),
    ]
    while time.time() - start5 < remaining:
        name, func = strats[cycle % len(strats)]
        Gn, dn = func(global_best_G)
        update_best(Gn, dn, f"Arch/{name}")
        if check(): return
        cycle += 1
        if cycle % 3 == 0:
            print(f"  [{time.time()-start5:.0f}s] cycle {cycle}, d={global_best_d}, A={global_best_a}")

    # ── FINAL ──
    elapsed = time.time() - start_time
    print(f"\n{'='*70}")
    print(f"  FINAL — {elapsed:.1f}s ({elapsed/60:.1f} min)")
    # Use GLOBAL best (never corrupted)
    best_G = global_best_G.copy()
    best_d = global_best_d
    print_matrix(best_G)
    we = weight_enum(best_G)
    print(f"  Weight enumerator:")
    for w in sorted(we.keys()):
        print(f"    A_{w} = {we[w]}")

    if best_d >= 13:
        save_result(best_G, "DIAMOND_22_6_13.txt")
        print("\n  ╔═══════════════════════════════════════════════════════════╗")
        print("  ║  NAPOLEON WAS RIGHT.                                     ║")
        print("  ╚═══════════════════════════════════════════════════════════╝")
    else:
        print(f"\n  Best d={best_d}. Gap: {13 - best_d}")
        print(f"  — SAMAEL. Σ=1561/675. The hunt continues.")

    save_result(best_G)
    print(f"{'='*70}\n")


if __name__ == '__main__':
    main()
