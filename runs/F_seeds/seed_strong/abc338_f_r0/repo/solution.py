import sys
import os
from operator import add

INF = float("inf")

C_SRC = r"""
#include <stdint.h>
#include <stdlib.h>
#define BIG 1000000000
/* d: n*n row-major closure (BIG = unreachable). Returns best cost, or BIG if none. */
int solve_dp(int n, const int *d, int *dp) {
    int full = (1 << n) - 1;
    /* dp[mask*n + v] */
    for (long long i = 0; i < (long long)(full + 1) * n; i++) dp[i] = BIG;
    for (int v = 0; v < n; v++) dp[(1 << v) * n + v] = 0;
    for (int mask = 1; mask <= full; mask++) {
        if ((mask & (mask - 1)) == 0) continue;
        for (int v = 0; v < n; v++) {
            if (!(mask >> v & 1)) continue;
            int pm = mask ^ (1 << v);
            const int *prow = dp + (long long)pm * n;
            int best = BIG;
            for (int u = 0; u < n; u++) {
                if (!(pm >> u & 1)) continue;
                int pv = prow[u];
                if (pv >= BIG) continue;
                int c = d[u * n + v];
                if (c >= BIG) continue;
                int s = pv + c;
                if (s < best) best = s;
            }
            dp[(long long)mask * n + v] = best;
        }
    }
    int ans = BIG;
    for (int v = 0; v < n; v++) {
        int x = dp[(long long)full * n + v];
        if (x < ans) ans = x;
    }
    return ans;
}
"""


def try_c_kernel(n, dmat):
    try:
        import ctypes
        import tempfile
        import subprocess
        tmpdir = tempfile.mkdtemp()
        src = os.path.join(tmpdir, "k.c")
        lib = os.path.join(tmpdir, "k.so")
        with open(src, "w") as f:
            f.write(C_SRC)
        subprocess.run(["gcc", "-O2", "-shared", "-fPIC", src, "-o", lib],
                       check=True, stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, timeout=30)
        cdll = ctypes.CDLL(lib)
        fn = cdll.solve_dp
        fn.restype = ctypes.c_int
        BIG = 1000000000
        flat = [BIG if x == INF else int(x) for row in dmat for x in row]
        arr_d = (ctypes.c_int * (n * n))(*flat)
        arr_dp = (ctypes.c_int * ((1 << n) * n))()
        res = fn(n, arr_d, arr_dp)
        return res
    except Exception:
        return None


def py_dp(n, d):
    col = [[d[u][v] for u in range(n)] for v in range(n)]
    full = (1 << n) - 1
    dp = [None] * (1 << n)
    blank = [INF] * n
    for v in range(n):
        row = blank[:]
        row[v] = 0
        dp[1 << v] = row
    for mask in range(1, full + 1):
        if mask & (mask - 1) == 0:
            continue
        row = blank[:]
        mm = mask
        while mm:
            lb = mm & -mm
            v = lb.bit_length() - 1
            mm ^= lb
            prev = dp[mask ^ lb]
            row[v] = min(map(add, prev, col[v]))
        dp[mask] = row
    return min(dp[full])


def main():
    data = sys.stdin.buffer.read().split()
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
    res = try_c_kernel(n, d)
    if res is not None:
        ans = None if res >= 1000000000 else res
    else:
        ans = py_dp(n, d)
        if ans == INF:
            ans = None
    if ans is None:
        print("No")
    else:
        print(int(ans))


main()
