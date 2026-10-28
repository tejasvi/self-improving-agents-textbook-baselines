import sys
from operator import mul

def main():
    data = sys.stdin.buffer.read().split()
    MOD = 998244353
    n = int(data[0]); m = int(data[1])
    INF = n + 5
    # minR[k][L] = min R among conditions with X=k and given L
    minR = [[INF] * (n + 2) for _ in range(n + 2)]
    idx = 2
    for _ in range(m):
        L = int(data[idx]); R = int(data[idx + 1]); X = int(data[idx + 2])
        idx += 3
        if R < minR[X][L]:
            minR[X][L] = R
    # bad[k][l] = min R over conditions with X=k, L>=l
    bad = [[INF] * (n + 2) for _ in range(n + 2)]
    for k in range(1, n + 1):
        cur = INF
        row = minR[k]
        brow = bad[k]
        for l in range(n, 0, -1):
            if row[l] < cur:
                cur = row[l]
            brow[l] = cur

    inv = [0, 1] + [0] * (n)
    for i in range(2, n + 2):
        inv[i] = (MOD - (MOD // i) * inv[MOD % i] % MOD) % MOD

    # G[s][e] = g over segment [s,e]; H[e][s] = same transposed. Empty segments = 1.
    G = [[0] * (n + 2) for _ in range(n + 2)]
    H = [[0] * (n + 2) for _ in range(n + 2)]
    for s in range(1, n + 2):
        G[s][s - 1] = 1
        H[s - 1][s] = 1

    for l in range(n, 0, -1):
        # kill events: at r = t, zero W[k] for k with bad[k][l] == t
        kill = [[] for _ in range(n + 2)]
        for k in range(l, n + 1):
            t = bad[k][l]
            if t <= n:
                kill[t].append(k)
        W = [0] * (n + 2)
        W[l] = 1
        Grow = G[l]
        for r in range(l, n + 1):
            for k in kill[r]:
                W[k] = 0
            s = sum(map(mul, W[l:r + 1], H[r][l + 1:r + 2])) % MOD
            val = s * inv[r - l + 1] % MOD
            Grow[r] = val
            H[r][l] = val
            W[r + 1] = val
    ans = G[1][n]
    fact = 1
    for i in range(1, n + 1):
        fact = fact * i % MOD
    print(ans * fact % MOD)

main()
