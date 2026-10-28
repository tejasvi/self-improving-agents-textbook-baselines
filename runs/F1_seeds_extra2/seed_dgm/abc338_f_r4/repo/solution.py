import sys
import os
import ctypes
import tempfile
import subprocess

INF = 10**9 + 7  # sentinel; valid path sums lie within about +-4e8

C_SRC = r"""
#include <stdint.h>
#include <stdlib.h>
#define INF 1000000007
/* d: n*n row-major shortest distances (INF if unreachable). Returns best, or INF. */
int solve(int n, const int *d, int *dp) {
    int full = (1 << n) - 1;
    long long total = (long long)(1 << n) * n;
    for (long long i = 0; i < total; i++) dp[i] = INF;
    for (int v = 0; v < n; v++) dp[(1 << v) * n + v] = 0;
    for (int mask = 1; mask <= full; mask++) {
        const int *row = dp + (long long)mask * n;
        for (int v = 0; v < n; v++) {
            if (!((mask >> v) & 1)) continue;
            int cur = row[v];
            if (cur >= INF) continue;
            for (int u = 0; u < n; u++) {
                if ((mask >> u) & 1) continue;
                int w = d[v * n + u];
                if (w >= INF) continue;
                int nm = mask | (1 << u);
                int nv = cur + w;
                int *t = dp + (long long)nm * n + u;
                if (nv < *t) *t = nv;
            }
        }
    }
    int best = INF;
    for (int v = 0; v < n; v++) {
        int x = dp[(long long)full * n + v];
        if (x < best) best = x;
    }
    return best;
}
"""


def load_c_kernel():
    try:
        tmpdir = tempfile.mkdtemp()
        src = os.path.join(tmpdir, "k.c")
        lib = os.path.join(tmpdir, "k.so")
        with open(src, "w") as f:
            f.write(C_SRC)
        subprocess.run(["gcc", "-O2", "-shared", "-fPIC", "-o", lib, src],
                       check=True, capture_output=True, timeout=60)
        cdll = ctypes.CDLL(lib)
        fn = cdll.solve
        fn.restype = ctypes.c_int
        fn.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int),
                       ctypes.POINTER(ctypes.c_int)]
        return fn
    except Exception:
        return None


def solve_py(n, d):
    full = (1 << n) - 1
    dp = [[INF] * n for _ in range(1 << n)]
    for v in range(n):
        dp[1 << v][v] = 0
    for mask in range(1, full + 1):
        row = dp[mask]
        for v in range(n):
            cur = row[v]
            if cur >= INF or not (mask >> v) & 1:
                continue
            dv = d[v]
            for u in range(n):
                if (mask >> u) & 1 or dv[u] >= INF:
                    continue
                t = dp[mask | (1 << u)]
                nv = cur + dv[u]
                if nv < t[u]:
                    t[u] = nv
    return min(dp[full])


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    d = [[INF] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = 0
    p = 2
    for _ in range(m):
        u, v, w = int(data[p]) - 1, int(data[p + 1]) - 1, int(data[p + 2])
        p += 3
        if w < d[u][v]:
            d[u][v] = w
    # Floyd-Warshall (no negative cycles)
    for k in range(n):
        dk = d[k]
        for i in range(n):
            dik = d[i][k]
            if dik >= INF:
                continue
            di = d[i]
            for j in range(n):
                if dk[j] < INF and dik + dk[j] < di[j]:
                    di[j] = dik + dk[j]

    kernel = load_c_kernel() if n >= 12 else None
    if kernel is not None:
        flat = (ctypes.c_int * (n * n))(*[x for row in d for x in row])
        dp = (ctypes.c_int * ((1 << n) * n))()
        best = kernel(n, flat, dp)
    else:
        best = solve_py(n, d)

    if best >= INF:
        print("No")
    else:
        print(best)


if __name__ == "__main__":
    main()
