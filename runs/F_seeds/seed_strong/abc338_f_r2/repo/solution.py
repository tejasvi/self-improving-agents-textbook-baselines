import sys
import os
import ctypes
import subprocess
import tempfile
from operator import add

C_SRC = r"""
#include <stddef.h>
#define INF_V (1LL<<60)
/* d: n*n row-major, d[v*n+w] = shortest dist v->w (INF_V if unreachable).
   Returns min Hamiltonian-path cost in the metric closure, or INF_V-ish sentinel. */
long long solve(int n, const long long *d, long long *dp) {
    int full = (1 << n) - 1;
    size_t total = (size_t)(full + 1) * n;
    for (size_t i = 0; i < total; i++) dp[i] = INF_V;
    for (int v = 0; v < n; v++) dp[((size_t)1 << v) * n + v] = 0;
    for (int mask = 1; mask <= full; mask++) {
        const long long *row = dp + (size_t)mask * n;
        for (int w = 0; w < n; w++) {
            if (mask & (1 << w)) continue;
            long long best = INF_V * 4;
            for (int v = 0; v < n; v++) {
                if (!(mask & (1 << v))) continue;
                if (row[v] >= INF_V || d[v * n + w] >= INF_V) continue;
                long long c = row[v] + d[v * n + w];
                if (c < best) best = c;
            }
            if (best >= INF_V) continue;
            int nm = mask | (1 << w);
            long long *t = dp + (size_t)nm * n + w;
            if (best < *t) *t = best;
        }
    }
    long long ans = INF_V * 4;
    const long long *last = dp + (size_t)full * n;
    for (int v = 0; v < n; v++) if (last[v] < INF_V && last[v] < ans) ans = last[v];
    return ans;
}
"""


def floyd(n, d):
    for k in range(n):
        dk = d[k]
        for i in range(n):
            dik = d[i][k]
            if dik is None:
                continue
            di = d[i]
            for j in range(n):
                if dk[j] is None:
                    continue
                nv = dik + dk[j]
                if di[j] is None or nv < di[j]:
                    di[j] = nv
    return d


def py_solve(n, d):
    INF = float("inf")
    dd = [[INF if d[i][j] is None else d[i][j] for j in range(n)] for i in range(n)]
    cols = [[dd[v][w] for v in range(n)] for w in range(n)]
    full = (1 << n) - 1
    dp = [None] * (1 << n)
    for v in range(n):
        row = [INF] * n
        row[v] = 0
        dp[1 << v] = row
    for mask in range(1, full + 1):
        row = dp[mask]
        if row is None:
            continue
        for w in range(n):
            bit = 1 << w
            if mask & bit:
                continue
            best = min(map(add, row, cols[w]))
            nm = mask | bit
            tgt = dp[nm]
            if tgt is None:
                tgt = [INF] * n
                dp[nm] = tgt
            if best < tgt[w]:
                tgt[w] = best
        if mask != full:
            dp[mask] = None
    ans = min(dp[full])
    return None if ans == INF else int(ans)


def c_solve(n, d):
    tmpdir = tempfile.mkdtemp()
    src = os.path.join(tmpdir, "k.c")
    lib = os.path.join(tmpdir, "k.so")
    with open(src, "w") as f:
        f.write(C_SRC)
    subprocess.run(["gcc", "-O2", "-shared", "-fPIC", "-o", lib, src],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    cl = ctypes.CDLL(lib)
    cl.solve.restype = ctypes.c_longlong
    cl.solve.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p]
    INF_V = 1 << 60
    flat = (ctypes.c_longlong * (n * n))(*[
        INF_V if d[i][j] is None else d[i][j] for i in range(n) for j in range(n)])
    dp = (ctypes.c_longlong * ((1 << n) * n))()
    res = cl.solve(n, flat, dp)
    if res >= INF_V:
        return None
    return int(res)


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    d = [[None] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = 0
    p = 2
    for _ in range(m):
        u = int(data[p]) - 1
        v = int(data[p + 1]) - 1
        w = int(data[p + 2])
        p += 3
        if d[u][v] is None or w < d[u][v]:
            d[u][v] = w
    floyd(n, d)
    try:
        ans = c_solve(n, d)
    except Exception:
        ans = py_solve(n, d)
    print("No" if ans is None else ans)


main()
