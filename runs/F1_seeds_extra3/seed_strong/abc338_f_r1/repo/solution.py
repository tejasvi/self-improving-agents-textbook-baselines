import sys
import os
import ctypes
import tempfile
import subprocess
from operator import add

C_SRC = r"""
#include <stdlib.h>
#include <stdint.h>
#define INF ((int64_t)1 << 60)
int solve(int n, int64_t *d, int64_t *out) {
    for (int k = 0; k < n; k++)
        for (int i = 0; i < n; i++) {
            int64_t dik = d[i * n + k];
            if (dik >= INF) continue;
            for (int j = 0; j < n; j++) {
                int64_t dkj = d[k * n + j];
                if (dkj >= INF) continue;
                if (dik + dkj < d[i * n + j]) d[i * n + j] = dik + dkj;
            }
        }
    int full = (1 << n) - 1;
    size_t total = (size_t)(1 << n) * n;
    int64_t *dp = (int64_t *)malloc(sizeof(int64_t) * total);
    if (!dp) return 0;
    for (size_t i = 0; i < total; i++) dp[i] = INF;
    for (int s = 0; s < n; s++) dp[((size_t)1 << s) * n + s] = 0;
    for (int mask = 1; mask <= full; mask++) {
        for (int v = 0; v < n; v++) {
            if (!(mask >> v & 1)) continue;
            int64_t cur = dp[(size_t)mask * n + v];
            if (cur >= INF) continue;
            for (int u = 0; u < n; u++) {
                if (mask >> u & 1) continue;
                int64_t c = d[v * n + u];
                if (c >= INF) continue;
                size_t idx = (size_t)(mask | (1 << u)) * n + u;
                if (cur + c < dp[idx]) dp[idx] = cur + c;
            }
        }
    }
    int64_t best = INF;
    for (int v = 0; v < n; v++)
        if (dp[(size_t)full * n + v] < best) best = dp[(size_t)full * n + v];
    free(dp);
    if (best >= INF) return 0;
    *out = best;
    return 1;
}
"""


def load_c_solver():
    try:
        tmpdir = tempfile.mkdtemp()
        src = os.path.join(tmpdir, "dp.c")
        lib = os.path.join(tmpdir, "dp.so")
        with open(src, "w") as f:
            f.write(C_SRC)
        subprocess.run(["gcc", "-O2", "-shared", "-fPIC", "-o", lib, src],
                       check=True, stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, timeout=60)
        cdll = ctypes.CDLL(lib)
        fn = cdll.solve
        fn.restype = ctypes.c_int
        fn.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int64),
                       ctypes.POINTER(ctypes.c_int64)]
        return fn
    except Exception:
        return None


def py_solve(n, d, INF):
    for k in range(n):
        dk = d[k]
        for i in range(n):
            dik = d[i][k]
            if dik >= INF:
                continue
            di = d[i]
            for j in range(n):
                nd = dik + dk[j]
                if nd < di[j]:
                    di[j] = nd
    col = [[d[v][u] for v in range(n)] for u in range(n)]
    full = (1 << n) - 1
    dp = [None] * (1 << n)
    dp[0] = [INF] * n
    half = INF >> 1
    for mask in range(1, full + 1):
        row = [INF] * n
        for u in range(n):
            bit = 1 << u
            if mask & bit:
                if mask == bit:
                    row[u] = 0
                    continue
                prev = dp[mask ^ bit]
                if prev is None:
                    continue
                best = min(map(add, prev, col[u]))
                if best < half:
                    row[u] = best
        dp[mask] = row
    best = min(dp[full])
    return None if best >= half else best


def main():
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    INF = 1 << 60
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

    fn = load_c_solver()
    ans = None
    if fn is not None:
        flat = (ctypes.c_int64 * (n * n))()
        for i in range(n):
            for j in range(n):
                flat[i * n + j] = d[i][j]
        out = ctypes.c_int64(0)
        if fn(n, flat, ctypes.byref(out)):
            ans = out.value
    else:
        ans = py_solve(n, d, INF)
    print("No" if ans is None else ans)


main()
