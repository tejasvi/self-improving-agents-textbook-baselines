import sys

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    b = [int(x) for x in data[2:2 + n]]
    q = sum(1 for v in b if v == -1)
    total = pow(m, q, MOD)
    if n < 2:
        print(total % MOD)
        return

    BIG = m + 1
    # prefix min of fixed values over positions 0..k-1
    pref_min = [BIG] * (n + 1)
    for i in range(n):
        pref_min[i + 1] = min(pref_min[i], b[i]) if b[i] != -1 else pref_min[i]
    # suffix max of fixed values over positions k..n-1
    suf_max = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suf_max[i] = max(suf_max[i + 1], b[i]) if b[i] != -1 else suf_max[i + 1]
    # suffix count of -1 over positions k..n-1
    suf_cnt = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suf_cnt[i] = suf_cnt[i + 1] + (1 if b[i] == -1 else 0)

    L = m + 2
    # base[v] = m - v + 1 (mod), for v in 0..m+1 ; base[m+1] = 0
    base = [(m - v + 1) % MOD for v in range(L)]
    base[0] = 0  # unused (v>=1)
    inv = [0] * (m + 1)
    for u in range(1, m + 1):
        inv[u] = pow(u, MOD - 2, MOD)

    # X[v] = (m-v+1)^c for prefix count c of -1s; start c = 0
    X = [1] * L
    c = 0
    # Y[u] = u^d for suffix count d; start at k=1 -> suffix positions 1..n-1
    Y = [pow(u, suf_cnt[1], MOD) for u in range(m + 1)]
    d = suf_cnt[1]

    for k in range(1, n):
        # prefix is positions 0..k-1: add position k-1
        if b[k - 1] == -1:
            X = [x * bs % MOD for x, bs in zip(X, base)]
            c += 1
        # suffix is positions k..n-1: ensure Y matches suf_cnt[k]
        nd = suf_cnt[k]
        while d > nd:
            # remove a -1 from suffix: exponent decreases by 1
            Y = [y * iv % MOD for y, iv in zip(Y, inv)]
            Y[0] = 1 if d - 1 == 0 else 0
            d -= 1
        F = pref_min[k]  # prefix fixed min (BIG if none)
        G = suf_max[k]   # suffix fixed max (0 if none)
        hi = min(m, F)
        lo = max(1, G + 1)
        if lo > hi:
            continue
        # Pk[v] = X[v] if v <= F else 0, for v in 0..m+1
        cut = min(F, m + 1)
        Pk = X[:cut + 1] + [0] * (L - cut - 1)
        s = 0
        for v in range(lo, hi + 1):
            s += (Pk[v] - Pk[v + 1]) * Y[v - 1]
        total = (total + s) % MOD
    print(total % MOD)

main()
