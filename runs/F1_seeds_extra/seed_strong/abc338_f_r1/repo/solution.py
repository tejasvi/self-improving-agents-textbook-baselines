import sys
import os
import ctypes
import tempfile
import subprocess
from operator import add

INF = float("inf")

C_SRC = r"""
#include <stdint.h>
#include <stdlib.h>
#define BIG 1000000000
#define NONE (-(1LL << 62))
/* d: n*n row-major shortest distances (BIG = unreachable). Returns min walk, or -1 if none. */
long long solve(int n, const int *d) {
    int full = (1 << n) - 1;
    int *cur = (int *)malloc(sizeof(int) * (size_t)(full + 1) * n);
    if (!cur) return NONE;
    for (size_t i = 0; i < (size_t)(full + 1) * n; i++) cur[i] = BIG;
    for (int u = 0; u < n; u++) cur[(size_t)(1 << u) * n + u] = 0;
    for (int S = 1; S <= full; S++) {
        int *row = cur + (size_t)S * n;
        for (int u = 0; u < n; u++) {
            if (S & (1 << u)) continue;
            int best = BIG;
            for (int v = 0; v < n; v++) {
                if (row[v] >= BIG) continue;
                int dv = d[v * n + u];
                if (dv >= BIG) continue;
                int c = row[v] + dv;
                if (c < best) best = c;
            }
            if (best < BIG) {
                int *t = cur + (size_t)(S | (1 << u)) * n + u;
                if (best < *t) *t = best;
            }
        }
    }
    long long ans = NONE;
    int *row = cur + (size_t)full * n;
    for (int v = 0; v < n; v++) {
        if (row[v] >= BIG) continue;
        for (int w = 0; w < n; w++) {
            if (d[v * n + w] >= BIG) continue;
            long long val = (long long)row[v] + d[v * n + w];
            if (ans == NONE || val < ans) ans = val;
        }
    }
    free(cur);
    return ans;
}
"""


def try_c(n, dmat):
    """Return (ok, value). value None means no walk exists."""
    try:
        tmpdir = tempfile.mkdtemp()
        src = os.path.join(tmpdir, "walk.c")
        lib = os.path.join(tmpdir, "walk.so")
        with open(src, "w") as f:
            f.write(C_SRC)
        subprocess.run(["gcc", "-O2", "-shared", "-fPIC", "-o", lib, src],
                       check=True, capture_output=True, timeout=30)
        cdll = ctypes.CDLL(lib)
        cdll.solve.restype = ctypes.c_longlong
        arr = (ctypes.c_int * (n * n))()
        for i in range(n):
            for j in range(n):
                arr[i * n + j] = dmat[i][j]
        res = cdll.solve(n, arr)
        return True, (None if res == -(1 << 62) else res)
    except Exception:
        return False, None


def py_solve(n, d):
    full = (1 << n) - 1
    col = [[d[v][u] for v in range(n)] for u in range(n)]
    cur = [[INF] * n for _ in range(1 << n)]
    for u in range(n):
        cur[1 << u][u] = 0
    for S in range(1, full + 1):
        row = cur[S]
        if min(row) == INF:
            continue
        for u in range(n):
            bit = 1 << u
            if S & bit:
                continue
            best = min(map(add, row, col[u]))
            if best < INF:
                T = S | bit
                if best < cur[T][u]:
                    cur[T][u] = best
    ans = INF
    row = cur[full]
    for v in range(n):
        if row[v] == INF:
            continue
        for w in range(n):
            val = row[v] + d[v][w]
            if val < ans:
                ans = val
    return None if ans == INF else ans


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    d = [[INF] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = 0
    p = 2
    for _ in range(m):
        u = int(data[p]) - 1
        v = int(data[p + 1]) - 1
        w = int(data[p + 2])
        p += 3
        if w < d[u][v]:
            d[u][v] = w
    # Floyd-Warshall (no negative cycles)
    for k in range(n):
        dk = d[k]
        for i in range(n):
            dik = d[i][k]
            if dik == INF:
                continue
            di = d[i]
            for j in range(n):
                nv = dik + dk[j]
                if nv < di[j]:
                    di[j] = nv

    ok, res = try_c(n, [[int(x) if x != INF else 10**9 for x in row] for row in d])
    if not ok:
        res = py_solve(n, d)
    print("No" if res is None else res)


main()
