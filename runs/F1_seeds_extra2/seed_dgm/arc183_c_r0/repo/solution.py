import sys

MOD = 998244353


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    m = int(data[1])
    INF = 10 ** 9
    # MR[p][a] = min R (0-indexed) over constraints with X=p and L>=a.
    # Half-open interval [a,b) is blocked at p iff MR[p][a] < b.
    MR = [[INF] * (n + 1) for _ in range(n)]
    idx = 2
    for _ in range(m):
        L = int(data[idx]) - 1
        R = int(data[idx + 1]) - 1
        X = int(data[idx + 2]) - 1
        idx += 3
        if R < MR[X][L]:
            MR[X][L] = R
    for p in range(n):
        row = MR[p]
        for a in range(n - 1, -1, -1):
            if row[a + 1] < row[a]:
                row[a] = row[a + 1]

    fact = [1] * (n + 2)
    for i in range(1, n + 2):
        fact[i] = fact[i - 1] * i % MOD
    inv = [0, 1] + [0] * (n + 1)
    for i in range(2, n + 2):
        inv[i] = (MOD - (MOD // i) * inv[MOD % i] % MOD) % MOD

    # G[a][b] = F(a,b) / (b-a)!   for interval [a,b)
    # H[b][a-1] = same value; H[b][p] describes interval [p+1,b)
    G = [[0] * (n + 1) for _ in range(n + 1)]
    H = [[0] * (n + 1) for _ in range(n + 1)]
    for a in range(n + 1):
        G[a][a] = 1          # empty interval
    for b in range(n + 1):
        H[b][b - 1] = 1 if b >= 1 else 0   # empty interval [b,b)

    for a in range(n - 1, -1, -1):
        Ga = G[a]
        mr = MR  # mr[p] = MR[p][a]
        mra = [mr[p][a] for p in range(n)]
        for b in range(a + 1, n + 1):
            Hb = H[b]
            S = sum([g * h for g, h, t in zip(Ga[a:b], Hb[a:b], mra[a:b]) if t >= b]) % MOD
            L = b - a
            val = S * inv[L] % MOD  # F(a,b) = S*(L-1)!, /L! gives S/L
            Ga[b] = val
            if a >= 1:
                H[b][a - 1] = val

    ans = G[0][n] * fact[n] % MOD
    print(ans)


main()
