import sys
import numpy as np

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    b = [int(x) for x in data[2:2 + n]]
    q = sum(1 for x in b if x == -1)

    # vals index v in 0..m+1 (use v in 1..m); arrays of length m+2
    vs = np.arange(m + 2, dtype=np.int64)

    def prefix_factor(x):
        # allowed count in [v, m] for each v
        if x == -1:
            c = np.maximum(m - vs + 1, 0)
        else:
            c = (vs <= x).astype(np.int64)
        c[0] = 0
        return c

    def suffix_factor(x):
        # allowed count in [1, s] for each s
        if x == -1:
            d = vs.copy()
        else:
            d = (vs >= x).astype(np.int64)
        d[0] = 0
        return d

    # H[k] = product over positions j > k (1-indexed) of suffix factors, k = 0..n
    H = [None] * (n + 1)
    cur = np.ones(m + 2, dtype=np.int64)
    H[n] = cur.copy()
    for k in range(n - 1, -1, -1):
        # position k (0-indexed) is k+1 in 1-indexed; suffix after prefix length k+1 excludes it
        cur = (cur * suffix_factor(b[k])) % MOD
        H[k] = cur.copy()

    total = pow(m, q, MOD)
    G = np.ones(m + 2, dtype=np.int64)
    # prefix length k (1-indexed positions 1..k), k from 1..n-1
    for k in range(1, n):
        G = (G * prefix_factor(b[k - 1])) % MOD
        Hk = H[k]  # suffix positions k+1..n (1-indexed)
        # count = sum_{s=1}^{m} H_k(s) * G_k(s+1)
        s = np.arange(1, m + 1)
        term = (Hk[1:m + 1] * G[2:m + 2]) % MOD
        total = (total + int(term.sum() % MOD)) % MOD
    print(total % MOD)

main()
