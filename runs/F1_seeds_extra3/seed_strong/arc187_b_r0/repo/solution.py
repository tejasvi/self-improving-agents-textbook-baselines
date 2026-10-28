import sys

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    B = [int(x) for x in data[2:2 + n]]
    Q = sum(1 for x in B if x == -1)
    ans = pow(m, Q, MOD)
    if m == 1 or n < 2:
        print(ans % MOD)
        return

    # Cut k (1..n-1): prefix B[:k], suffix B[k:].
    # Components = 1 + #cuts, cut valid iff min(prefix) > max(suffix).
    # For cut k, let t = max(suffix) (value in 1..m):
    #   prefix: fixed > t, -1 free in (t, m]  -> (m-t)^qp
    #   suffix: fixed <= t, max exactly t
    #       -> [Rk<=t] t^qs - [Rk<=t-1] (t-1)^qs
    INF = m + 1
    qp = [0] * (n + 1)
    Lk = [INF] * (n + 1)
    for k in range(1, n + 1):
        x = B[k - 1]
        qp[k] = qp[k - 1] + (x == -1)
        Lk[k] = min(Lk[k - 1], x) if x != -1 else Lk[k - 1]
    qs = [0] * (n + 1)
    Rk = [0] * (n + 2)
    for k in range(n - 1, -1, -1):
        x = B[k]
        qs[k] = qs[k + 1] + (x == -1)
        Rk[k] = max(Rk[k + 1], x) if x != -1 else Rk[k + 1]

    ks = list(range(1, n))
    # Lk nonincreasing; Rk nonincreasing in k.
    total = 0
    for t in range(1, m + 1):
        # valid for term1: Lk[k] > t and Rk[k] <= t
        # valid for term2: Lk[k] > t and Rk[k] <= t-1
        # Lk[k] > t  <=> k <= K1 (prefix of ks); Rk[k] <= t <=> k >= K2
        K1 = 0
        while K1 < len(ks) and Lk[ks[K1]] > t:
            K1 += 1
        if K1 == 0:
            break  # Lk nonincreasing, larger t only shrinks; but keep simple
        # K2: first k with Rk[k] <= t ; Rk nonincreasing
        # Rk[k] <= t-1 is stricter
        lo1 = 1
        while lo1 < n and Rk[lo1] > t:
            lo1 += 1
        lo2 = 1
        while lo2 < n and Rk[lo2] > t - 1:
            lo2 += 1
        # term1 over k in [lo1, K1]; term2 over k in [lo2, K1]
        pt = [1] * (n + 1)
        pt1 = [1] * (n + 1)
        pb = [1] * (n + 1)
        for e in range(1, n + 1):
            pt[e] = pt[e - 1] * t % MOD
            pt1[e] = pt1[e - 1] * (t - 1) % MOD
            pb[e] = pb[e - 1] * (m - t) % MOD
        s = 0
        for k in range(lo1, K1 + 1):
            s += pt[qs[k]] * pb[qp[k]]
        for k in range(lo2, K1 + 1):
            s -= pt1[qs[k]] * pb[qp[k]]
        total = (total + s) % MOD
    ans = (ans + total) % MOD
    print(ans)

main()
