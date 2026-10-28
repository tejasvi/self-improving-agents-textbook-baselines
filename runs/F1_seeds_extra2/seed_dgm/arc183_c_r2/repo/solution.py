import sys

def main():
    data = sys.stdin.buffer.read().split()
    MOD = 998244353
    n, m = int(data[0]), int(data[1])
    INF = n + 5
    # G[X][L] = min R over constraints with this X and this L
    G = [[INF] * (n + 2) for _ in range(n + 2)]
    idx = 2
    for _ in range(m):
        L = int(data[idx]); R = int(data[idx + 1]); X = int(data[idx + 2])
        idx += 3
        if R < G[X][L]:
            G[X][L] = R
    # g[l][p] = min over L in [l,p] of G[p][L]
    g = [[INF] * (n + 2) for _ in range(n + 2)]
    for p in range(1, n + 1):
        cur = INF
        for l in range(p, 0, -1):
            if G[p][l] < cur:
                cur = G[p][l]
            g[l][p] = cur

    inv = [0, 1] + [0] * n
    for i in range(2, n + 1):
        inv[i] = (MOD - (MOD // i) * inv[MOD % i] % MOD) % MOD

    # E[l][r] = F[l][r] / (r-l+1)!, with empty intervals E = 1.
    # ET[r][l] = E[l][r] for convenient column access.
    E = [[0] * (n + 2) for _ in range(n + 2)]
    ET = [[0] * (n + 2) for _ in range(n + 2)]
    for i in range(1, n + 2):
        E[i][i - 1] = 1
        ET[i - 1][i] = 1  # E[i][i-1] stored at ET[i-1][i]

    for length in range(1, n + 1):
        for l in range(1, n - length + 2):
            r = l + length - 1
            gl = g[l]
            El = E[l]
            ETr = ET[r]
            total = 0
            # p ranges over l..r; left factor E[l][p-1] = El[p-1]; right factor E[p+1][r] = ETr[p+1]
            for p in range(l, r + 1):
                if gl[p] > r:
                    total += El[p - 1] * ETr[p + 1]
            val = total % MOD * inv[length] % MOD
            E[l][r] = val
            ET[r][l] = val
    fact_n = 1
    for i in range(1, n + 1):
        fact_n = fact_n * i % MOD
    print(E[1][n] * fact_n % MOD)

main()
