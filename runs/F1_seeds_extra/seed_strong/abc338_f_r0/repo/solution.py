import sys
import os
import ctypes
import tempfile
import subprocess
from array import array
from operator import add

INF = float('inf')

C_SRC = r"""
#include <stdlib.h>
#include <string.h>
/* D: n*n matrix, D[i*n+j] = shortest dist i->j, or BIG if unreachable.
   Returns min walk cost covering all vertices, or BIG if none. */
int solve(int n, const int *D, int BIG) {
    int full = (1 << n) - 1;
    size_t sz = (size_t)(full + 1) * n;
    int *dp = (int *)malloc(sz * sizeof(int));
    if (!dp) return BIG;
    for (size_t i = 0; i < sz; i++) dp[i] = BIG;
    for (int v = 0; v < n; v++) dp[((size_t)1 << v) * n + v] = 0;
    for (int mask = 1; mask <= full; mask++) {
        const int *row = dp + (size_t)mask * n;
        for (int v = 0; v < n; v++) {
            if (!(mask >> v & 1)) continue;
            int cur = row[v];
            if (cur >= BIG) continue;
            for (int u = 0; u < n; u++) {
                if (mask >> u & 1) continue;
                int d = D[v * n + u];
                if (d >= BIG) continue;
                int nm = mask | (1 << u);
                int *t = dp + (size_t)nm * n + u;
                if (cur + d < *t) *t = cur + d;
            }
        }
    }
    int ans = BIG;
    for (int v = 0; v < n; v++) {
        int x = dp[(size_t)full * n + v];
        if (x < ans) ans = x;
    }
    free(dp);
    return ans;
}
"""


def try_c(n, Dflat):
    """Compile and run the C DP. Returns the answer, or None if unavailable."""
    try:
        d = tempfile.mkdtemp()
        src = os.path.join(d, "dp.c")
        lib = os.path.join(d, "dp.so")
        with open(src, "w") as f:
            f.write(C_SRC)
        subprocess.run(["gcc", "-O2", "-shared", "-fPIC", "-o", lib, src],
                       check=True, timeout=30,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        cl = ctypes.CDLL(lib)
        cl.solve.restype = ctypes.c_int
        cl.solve.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_int]
        BIG = 1000000000
        arr = array('i', [BIG if x == INF else int(x) for x in Dflat])
        buf, _ = arr.buffer_info()
        res = cl.solve(n, buf, BIG)
        return None if res >= BIG else res
    except Exception:
        return None


def py_dp(n, D):
    """Pure-Python Held-Karp fallback."""
    full = (1 << n) - 1
    dp = array('d', [INF]) * ((full + 1) * n)
    for v in range(n):
        dp[(1 << v) * n + v] = 0.0
    col = [[D[v][u] for v in range(n)] for u in range(n)]
    for mask in range(1, full + 1):
        base = mask * n
        row = dp[base:base + n]
        if min(row) == INF:
            continue
        for u in range(n):
            bit = 1 << u
            if mask & bit:
                continue
            best = min(map(add, row, col[u]))
            if best == INF:
                continue
            t = (mask | bit) * n + u
            if best < dp[t]:
                dp[t] = best
    ans = min(dp[full * n + v] for v in range(n))
    return None if ans == INF else int(ans)


def main():
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
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
    # Floyd-Warshall (no negative cycles => valid shortest paths)
    for k in range(n):
        Dk = D[k]
        for i in range(n):
            dik = D[i][k]
            if dik == INF:
                continue
            Di = D[i]
            for j in range(n):
                t = dik + Dk[j]
                if t < Di[j]:
                    Di[j] = t
    Dflat = [D[i][j] for i in range(n) for j in range(n)]
    ans = try_c(n, Dflat)
    if ans is None:
        ans = py_dp(n, D)
    print("No" if ans is None else ans)


main()
