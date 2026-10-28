import sys
import os
import ctypes
import tempfile
import subprocess

C_SRC = r"""
#include <stdint.h>
#define INF_V ((int64_t)4000000000000000000LL)
/* D: n*n row-major shortest distances, INF_V for unreachable.
   Returns min Hamiltonian-path cost over all start vertices, or INF_V. */
int64_t solve(int n, const int64_t *D) {
    int full = (1 << n) - 1;
    int64_t *dp = (int64_t *)malloc(sizeof(int64_t) * (size_t)(1 << n) * n);
    if (!dp) return INF_V;
    for (size_t i = 0; i < (size_t)(1 << n) * n; i++) dp[i] = INF_V;
    for (int v = 0; v < n; v++) dp[((size_t)1 << v) * n + v] = 0;
    for (int mask = 1; mask <= full; mask++) {
        for (int v = 0; v < n; v++) {
            int64_t cur = dp[(size_t)mask * n + v];
            if (cur >= INF_V) continue;
            for (int w = 0; w < n; w++) {
                if (mask >> w & 1) continue;
                int64_t d = D[v * n + w];
                if (d >= INF_V) continue;
                size_t idx = (size_t)(mask | (1 << w)) * n + w;
                if (cur + d < dp[idx]) dp[idx] = cur + d;
            }
        }
    }
    int64_t best = INF_V;
    for (int v = 0; v < n; v++) {
        int64_t c = dp[(size_t)full * n + v];
        if (c < best) best = c;
    }
    free(dp);
    return best;
}
"""


def load_c_solver():
    try:
        tmpdir = tempfile.mkdtemp()
        src = os.path.join(tmpdir, "h.c")
        lib = os.path.join(tmpdir, "h.so")
        with open(src, "w") as f:
            f.write("#include <stdlib.h>\n" + C_SRC)
        subprocess.run(["gcc", "-O2", "-shared", "-fPIC", "-o", lib, src],
                       check=True, stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, timeout=20)
        cdll = ctypes.CDLL(lib)
        fn = cdll.solve
        fn.restype = ctypes.c_int64
        fn.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int64)]
        return fn
    except Exception:
        return None


def py_solve(n, D, INF):
    adj = [[(w, D[v][w]) for w in range(n) if w != v and D[v][w] != INF]
           for v in range(n)]
    cur_layer = {}
    for v in range(n):
        cur_layer[1 << v] = [INF] * n
        cur_layer[1 << v][v] = 0
    for _ in range(n - 1):
        nxt = {}
        for mask, row in cur_layer.items():
            for v in range(n):
                c0 = row[v]
                if c0 == INF:
                    continue
                for w, d in adj[v]:
                    b = 1 << w
                    if mask & b:
                        continue
                    nm = mask | b
                    r = nxt.get(nm)
                    if r is None:
                        r = [INF] * n
                        nxt[nm] = r
                    c = c0 + d
                    if c < r[w]:
                        r[w] = c
        cur_layer = nxt
    row = cur_layer.get((1 << n) - 1)
    return min(row) if row else INF


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    INF = float("inf")
    D = [[INF] * n for _ in range(n)]
    for i in range(n):
        D[i][i] = 0
    p = 2
    for _ in range(m):
        u = int(data[p]) - 1
        v = int(data[p + 1]) - 1
        w = int(data[p + 2])
        p += 3
        if w < D[u][v]:
            D[u][v] = w
    # Floyd-Warshall (no negative cycles, so this gives true shortest paths).
    for k in range(n):
        Dk = D[k]
        for i in range(n):
            dik = D[i][k]
            if dik == INF:
                continue
            Di = D[i]
            for j in range(n):
                nd = dik + Dk[j]
                if nd < Di[j]:
                    Di[j] = nd
    # A covering walk's first-visit order is a permutation, and its cost is at
    # least the sum of shortest distances between consecutive first visits;
    # conversely every permutation is realizable. So answer = min Hamiltonian
    # path cost under shortest distances D.
    fn = load_c_solver()
    if fn is not None:
        BIG = 4000000000000000000
        flat = (ctypes.c_int64 * (n * n))()
        for i in range(n):
            for j in range(n):
                flat[i * n + j] = BIG if D[i][j] == INF else int(D[i][j])
        ans = fn(n, flat)
        if ans >= BIG:
            print("No")
        else:
            print(ans)
    else:
        ans = py_solve(n, D, INF)
        print("No" if ans == INF else ans)


main()
