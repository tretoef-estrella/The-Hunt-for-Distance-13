#!/usr/bin/env python3
"""
PROYECTO ESTRELLA — 108 DOCTRINES ENGINE v15 (THE ITALIAN JOB)
[22,6,13]_4 over GF(4) — VERTICAL COLLAPSE PROTOCOL

The Italian Job:
1. Lock 5 rows. 100% firepower on row 6.
2. Cycle through ALL bases of the A42 code.
   Each basis change exposes a DIFFERENT row 6.
3. Reject anything below floor (no sustentation).
4. Pitbull on any crack below A₁₂=42.

    cd ~/Downloads && python3 estrella_108_v15.py

Rafa — The Architect + Claude (SAMAEL Beast 10)
Σ = 1561/675 ≈ 2.31 | 73 mechanisms | 10 beasts
"""

import numpy as np
import ctypes, time, os, platform, subprocess, tempfile

GF4_ADD = np.array([[0,1,2,3],[1,0,3,2],[2,3,0,1],[3,2,1,0]], dtype=np.uint8)
GF4_MUL = np.array([[0,0,0,0],[0,1,2,3],[0,2,3,1],[0,3,1,2]], dtype=np.uint8)
GF4_INV = np.array([0,1,3,2], dtype=np.uint8)

_C_SOURCE = r"""
#include <stdint.h>
#include <string.h>
static const uint8_t GA[4][4]={{0,1,2,3},{1,0,3,2},{2,3,0,1},{3,2,1,0}};
static const uint8_t GM[4][4]={{0,0,0,0},{0,1,2,3},{0,2,3,1},{0,3,1,2}};

__attribute__((visibility("default")))
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

__attribute__((visibility("default")))
int min_distance_early(const uint8_t*G,int k,int n,int thr){
    int total=1;for(int i=0;i<k;i++)total*=4;uint8_t cw[256],v[10];
    for(int idx=1;idx<total;idx++){
        int tmp=idx;for(int j=k-1;j>=0;j--){v[j]=tmp%4;tmp/=4;}
        memset(cw,0,n);
        for(int j=0;j<k;j++){if(v[j]==0)continue;const uint8_t*row=G+j*n;
            for(int c=0;c<n;c++)cw[c]=GA[cw[c]][GM[v[j]][row[c]]];}
        int w=0;for(int c=0;c<n;c++){if(cw[c])w++;if(n-c+w<thr)goto skip;}
        if(w<thr)return w;skip:;
    }return thr;}
"""

_LIB = None
def _compile():
    global _LIB
    if _LIB is not None: return True
    try:
        td = tempfile.mkdtemp()
        src = os.path.join(td,"gf4.c")
        ext = ".dylib" if platform.system()=="Darwin" else ".so"
        lib = os.path.join(td,"gf4"+ext)
        with open(src,"w") as f: f.write(_C_SOURCE)
        r = subprocess.run(["gcc","-O3","-shared","-fPIC","-o",lib,src], capture_output=True, timeout=30)
        if r.returncode==0:
            _LIB = ctypes.CDLL(lib)
            _LIB.min_distance.restype = ctypes.c_int
            _LIB.min_distance.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
            _LIB.min_distance_early.restype = ctypes.c_int
            _LIB.min_distance_early.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int]
            return True
    except: pass
    return False

_compile()  # compile at import

def min_dist_full(G):
    G_c = np.ascontiguousarray(G, dtype=np.uint8); k,n = G_c.shape
    if _LIB:
        cnt = ctypes.c_int(0)
        d = _LIB.min_distance(G_c.ctypes.data, k, n, ctypes.byref(cnt))
        return d, cnt.value
    total=4**k; md,mc=n+1,0
    for idx in range(1,total):
        tmp=idx; v=[]
        for _ in range(k): v.append(tmp%4); tmp//=4
        v=v[::-1]; cw=np.zeros(n,dtype=np.uint8)
        for j in range(k):
            if v[j]==0: continue
            cw=GF4_ADD[cw,GF4_MUL[v[j]][G[j]]]
        w=int(np.count_nonzero(cw))
        if w<md: md,mc=w,1
        elif w==md: mc+=1
    return md,mc

def min_dist_early(G, thr=13):
    G_c = np.ascontiguousarray(G, dtype=np.uint8); k,n = G_c.shape
    if _LIB: return _LIB.min_distance_early(G_c.ctypes.data, k, n, thr)
    d,_ = min_dist_full(G_c); return d if d<thr else thr

def systematic_form(G):
    k,n = G.shape; A = G.copy()
    for col in range(k):
        pivot=None
        for row in range(col,k):
            if A[row,col]!=0: pivot=row; break
        if pivot is None: return None  # singular
        A[[col,pivot]]=A[[pivot,col]]
        A[col]=GF4_MUL[GF4_INV[A[col,col]]][A[col]]
        for row in range(k):
            if row!=col and A[row,col]!=0:
                A[row]=GF4_ADD[A[row],GF4_MUL[A[row,col]][A[col]]]
    return A

def print_mat(G, prefix="  "):
    s={0:"0",1:"1",2:"ω",3:"ω²"}
    for i in range(G.shape[0]):
        print(prefix+"[" + " ".join(s[G[i,c]] for c in range(G.shape[1])) + "]")

# ═══════════════════════════════════════════════════════════════
# SEEDS
# ═══════════════════════════════════════════════════════════════
SEED_A42 = np.array([
    [1,1,0,0,0,0, 3,2,1,1,2,2,0,1,0,1,0,3,0,0,3,3],
    [0,0,0,0,0,0, 2,2,0,0,1,3,3,2,2,2,1,3,1,0,2,2],
    [0,2,1,0,0,0, 3,2,3,2,0,3,0,1,1,0,2,2,2,1,0,2],
    [0,0,0,1,0,0, 2,0,3,3,3,0,1,2,2,1,0,0,3,2,2,1],
    [0,3,0,0,1,0, 3,3,2,0,3,3,2,0,1,2,1,2,1,2,0,0],
    [0,0,0,0,0,1, 0,0,2,1,3,0,3,1,3,0,2,2,1,2,2,1],
], dtype=np.uint8)

SEED_A48 = np.array([
    [1,0,0,0,0,0, 3,2,1,1,2,2,0,1,0,1,0,3,0,0,3,3],
    [0,1,0,0,0,0, 2,2,0,0,1,3,3,2,2,2,1,3,1,0,2,2],
    [0,0,1,0,0,0, 3,2,3,2,0,3,0,1,1,0,2,2,2,1,0,2],
    [0,0,0,1,0,0, 2,0,3,3,3,0,1,2,2,1,0,0,3,2,2,1],
    [0,0,0,0,1,0, 3,3,2,0,3,3,2,0,1,2,1,2,1,2,0,0],
    [0,0,0,0,0,1, 0,0,2,1,3,0,3,1,3,0,2,2,1,2,2,1],
], dtype=np.uint8)


# ═══════════════════════════════════════════════════════════════
# BASE GENERATION — All views of the A42 code
# ═══════════════════════════════════════════════════════════════

def generate_bases(G_seed):
    """Generate distinct (base5, row6) pairs by basis changes + column permutations."""
    k,n = G_seed.shape
    bases = []
    seen = set()
    
    def try_add(G_new, tag):
        G_sys = systematic_form(G_new)
        if G_sys is None: return
        ident = np.eye(k, dtype=np.uint8)
        if not np.array_equal(G_sys[:,:k], ident): return
        key = G_sys[:5].tobytes()
        if key in seen: return
        seen.add(key)
        bases.append((tag, G_sys[:5].copy(), G_sys[5].copy()))
    
    # Original
    try_add(G_seed, "orig")
    
    # All single row additions: g_i += s*g_j
    for i in range(k):
        for j in range(k):
            if i==j: continue
            for s in range(1,4):
                G = G_seed.copy()
                G[i] = GF4_ADD[G[i], GF4_MUL[s][G[j]]]
                try_add(G, f"r{i}+={s}r{j}")
    
    # All row swaps
    for i in range(k):
        for j in range(i+1,k):
            G = G_seed.copy()
            G[[i,j]] = G[[j,i]]
            try_add(G, f"swap{i}{j}")
    
    # Double row additions
    for i in range(k):
        for j in range(k):
            if i==j: continue
            for s1 in range(1,4):
                G = G_seed.copy()
                G[i] = GF4_ADD[G[i], GF4_MUL[s1][G[j]]]
                for i2 in range(k):
                    for j2 in range(k):
                        if i2==j2: continue
                        for s2 in range(1,4):
                            G2 = G.copy()
                            G2[i2] = GF4_ADD[G2[i2], GF4_MUL[s2][G2[j2]]]
                            try_add(G2, f"r{i}+={s1}r{j}_r{i2}+={s2}r{j2}")
    
    # Column permutations (random sample)
    for _ in range(200):
        perm = np.random.permutation(n)
        G = G_seed[:, perm]
        try_add(G, f"colperm")
    
    return bases


def sweep(base5, row6_start, tag, d_floor, a_record, time_limit=120):
    """Vertical Collapse: random row 6, Pitbull on improvement."""
    n = base5.shape[1]
    best_d, best_a = d_floor, a_record
    best_G = np.vstack([base5, row6_start.reshape(1,-1)])
    best_row6 = row6_start.copy()
    pitbull = False; p_row = None; p_count = 0
    start = time.time(); tested = 0
    
    while time.time()-start < time_limit:
        if pitbull and p_row is not None:
            row6 = p_row.copy()
            for _ in range(np.random.randint(1,3)):
                row6[np.random.randint(0,n)] = np.random.randint(0,4)
            p_count += 1
            if p_count > 20000: pitbull=False; p_count=0
        else:
            row6 = np.random.randint(0,4,size=n).astype(np.uint8)
        
        if np.all(row6==0): continue
        G6 = np.vstack([base5, row6.reshape(1,-1)]); tested += 1
        d = min_dist_early(G6, d_floor)
        if d < d_floor: continue
        
        d_full, a_full = min_dist_full(G6)
        if d_full >= 13:
            print(f"\n    ★★★ DIAMOND [22,6,{d_full}]_4 ★★★ base={tag}, tested={tested}")
            print_mat(G6)
            return G6, d_full, a_full, True
        
        if d_full > best_d or (d_full==best_d and a_full < best_a):
            old_a = best_a
            best_d, best_a, best_G = d_full, a_full, G6.copy()
            best_row6 = row6.copy()
            print(f"    [{tag}] A_{best_d}={best_a} (was {old_a}) [{tested}/{time.time()-start:.1f}s]")
            if best_a < a_record:
                pitbull=True; p_row=row6.copy(); p_count=0
                print(f"    >>> PITBULL on A_{best_d}={best_a}")
                print_mat(best_G)
    
    e=time.time()-start; r=tested/e if e>0 else 0
    print(f"    [{tag}] {tested} ({r:.0f}/s) best A_{best_d}={best_a}")
    return best_G, best_d, best_a, False


def heat_polish(G_in, time_limit=45):
    """Heat-seeker gradient polish."""
    k,n = G_in.shape; G=G_in.copy()
    d_cur, a_cur = min_dist_full(G)
    bd,ba,bG = d_cur,a_cur,G.copy()
    start=time.time()
    while time.time()-start < time_limit:
        imp=False
        for r in range(k):
            for c in range(n):
                old=G[r,c]
                for v in range(4):
                    if v==old: continue
                    G[r,c]=v
                    d=min_dist_early(G,bd)
                    if d>=bd:
                        df,af=min_dist_full(G)
                        if df>bd or (df==bd and af<ba):
                            bd,ba,bG=df,af,G.copy()
                            if df>=13: return bG,bd,ba
                            a_cur=af; imp=True; break
                    G[r,c]=old
                else: G[r,c]=old
        if not imp: break
    return bG,bd,ba


def run():
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║  PROYECTO ESTRELLA — 108 DOCTRINES ENGINE v15                ║
    ║  THE ITALIAN JOB — Vertical Collapse Protocol                ║
    ║  Σ = 1561/675 | Lock 5, sweep row 6, cycle ALL bases        ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    if _LIB: print("  C kernel: LOADED")
    else: print("  C kernel: FAILED — Python fallback (slow)")
    
    d42,a42 = min_dist_full(SEED_A42)
    print(f"  A42 seed: [22,6,{d42}]_4, A_{d42}={a42}")
    d48,a48 = min_dist_full(SEED_A48)
    print(f"  A48 seed: [22,6,{d48}]_4, A_{d48}={a48}")
    
    print(f"\n[GENERATING BASES]")
    bases = generate_bases(SEED_A42)
    n1 = len(bases)
    bases2 = generate_bases(SEED_A48)
    seen = {b.tobytes() for _,b,_ in bases}
    for t,b,r in bases2:
        if b.tobytes() not in seen:
            seen.add(b.tobytes()); bases.append(("48_"+t,b,r))
    print(f"  {n1} bases from A42, {len(bases)} total")
    
    # Speed
    t0=time.time()
    for _ in range(200): min_dist_early(SEED_A42,12)
    spd=200/(time.time()-t0)
    print(f"  Speed: {spd:.0f} early/sec")
    
    gd,ga,gG = d42, a42, SEED_A42.copy()
    cycle=0; t_start=time.time()
    
    while True:
        cycle+=1
        np.random.shuffle(bases)
        print(f"\n{'='*60}")
        print(f"  CYCLE {cycle} | Record: A_{gd}={ga} | Bases: {len(bases)} | {time.time()-t_start:.0f}s")
        print(f"{'='*60}")
        
        for bi,(tag,b5,r6) in enumerate(bases):
            tl = 30 if cycle<=2 else 20
            print(f"\n  [{bi+1}/{len(bases)}] {tag}")
            Go,do_,ao,found = sweep(b5, r6, tag, gd, ga, time_limit=tl)
            
            if found:
                gG=Go.copy()
                with open("DIAMOND_22_6_13.txt","w") as f:
                    f.write(f"DIAMOND [22,6,{do_}]_4\n{time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    for i in range(Go.shape[0]):
                        f.write("[" + " ".join(str(Go[i,c]) for c in range(Go.shape[1])) + "]\n")
                print(f"\n  ★★★ SAVED DIAMOND_22_6_13.txt ★★★")
                return
            
            if do_>gd or (do_==gd and ao<ga):
                gd,ga,gG = do_,ao,Go.copy()
                print(f"\n  >>> RECORD A_{gd}={ga} — polishing...")
                Gp,dp,ap = heat_polish(gG, 15)
                if dp>gd or (dp==gd and ap<ga):
                    gd,ga,gG = dp,ap,Gp.copy()
                    print(f"  >>> POLISHED: A_{gd}={ga}")
                    print_mat(gG)
                if gd>=13:
                    with open("DIAMOND_22_6_13.txt","w") as f:
                        f.write(f"DIAMOND\n")
                        for i in range(gG.shape[0]):
                            f.write(" ".join(str(gG[i,c]) for c in range(gG.shape[1]))+"\n")
                    print(f"  ★★★ DIAMOND ★★★"); return
        
        print(f"\n  Cycle {cycle} done. A_{gd}={ga}. {time.time()-t_start:.0f}s total.")

if __name__=='__main__':
    run()
