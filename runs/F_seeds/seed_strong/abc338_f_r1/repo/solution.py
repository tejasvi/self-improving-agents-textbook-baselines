import sys
import os
import tempfile
import subprocess
from operator import add

C_SRC = r"""
#include <stdlib.h>
long long held(int n, const long long *D, long long BIG, int *ok) {
    int full = (1 << n) - 1;
    size_t total = (size_t)(full + 1) * n;
    long long *f = (long long *)malloc(sizeof(long long) * total);
    if (!f) { *ok = 0; return 0; }
    for (size_t i = 0; i < total; i++) f[i] = BIG;
    for (int w = 0; w < n; w++) f[((size_t)1 << w) * n + w] = 0;
    for (int mask = 1; mask <= full; mask++) {
        for (int w = 0; w < n; w++) {
            if (!((mask >> w) & 1)) continue;
            int pm = mask ^ (1 << w);
            if (!pm) continue;
            long long best = BIG;
            const long long *row = f + (size_t)pm * n;
            for (int v = 0; v < n; v++) {
                if (row[v] >= BIG) continue;
                long long c = row[v] + D[v * n + w];
                if (c < best) best = c;
            }
            f[(size_t)mask * n + w] = best;
        }
    }
    long long best = BIG;
    for (int w = 0; w < n; w++)
        if (f[(size_t)full * n + w] < best) best = f[(size_t)full * n + w];
    free(f);
    *ok = best < BIG / 2;
    return best;
}
"""


def run_c(n, D, BIG):
    """Return (ok, value) using compiled C kernel, or None if unavailable."""
    import ctypes
    tmpdir = tempfile.mkdtemp()
    src = os.path.join(tmpdir, "dp.c")
    lib = os.path.join(tmpdir, "dp.so")
    with open(src, "w") as fh:
        fh.write(C_SRC)
    subprocess.run(["gcc", "-O2", "-shared", "-fPIC", "-o", lib, src],
                   check=True, stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, timeout=30)
    cl = ctypes.CDLL(lib)
    cl.held.restype = ctypes.c_longlong
    cl.held.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_longlong),
                        ctypes.c_longlong, ctypes.POINTER(ctypes.c_int)]
    flat = (ctypes.c_longlong * (n * n))(*[D[i][j] for i in range(n) for j in range(n)])
    ok = ctypes.c_int(0)
    val = cl.held(n, flat, BIG, ctypes.byref(ok))
    return ok.value, val


def py_dp(n, D, BIG):
    Dcol = [[D[v][w] for v in range(n)] for w in range(n)]
    full = (1 << n) - 1
    f = [BIG] * ((1 << n) * n)
    for w in range(n):
        f[(1 << w) * n + w] = 0
    for mask in range(1, full + 1):
        base_m = mask * n
        mm = mask
        while mm:
            low = mm & -mm
            mm ^= low
            w = low.bit_length() - 1
            pm = mask ^ low
            if pm == 0:
                continue
            b = pm * n
            best = min(map(add, f[b:b + n], Dcol[w]))
            if best < BIG // 2:
                f[base_m + w] = best
    best = min(f[full * n + w] for w in range(n))
    return (best < BIG // 2), best


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    BIG = 10 ** 15
    D = [[BIG] * n for _ in range(n)]
    for i in range(n):
        D[i][i] = 0
    p = 2
    for _ in range(m):
        u, v, w = int(data[p]) - 1, int(data[p + 1]) - 1, int(data[p + 2])
        p += 3
        if w < D[u][v]:
            D[u][v] = w
    # Floyd-Warshall (no negative cycles)
    for k in range(n):
        Dk = D[k]
        for i in range(n):
            dik = D[i][k]
            if dik >= BIG:
                continue
            Di = D[i]
            for j in range(n):
                c = dik + Dk[j]
                if c < Di[j]:
                    Di[j] = c

    res = None
    try:
        res = run_c(n, D, BIG)
    except Exception:
        res = None
    if res is None:
        res = py_dp(n, D, BIG)
    ok, val = res
    if not ok:
        print("No")
    else:
        print(val)


main()
