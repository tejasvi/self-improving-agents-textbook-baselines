import sys

def main():
    data = sys.stdin.buffer.read().split()
    MOD = 998244353
    n = int(data[0]); m = int(data[1])
    INF = n + 5
    # best[p][L] = min R over conditions with X=p and left endpoint L
    best = [[INF] * (n + 2) for _ in range(n + 2)]
    idx = 2
    for _ in range(m):
        L = int(data[idx]); R = int(data[idx + 1]); X = int(data[idx + 2])
        idx += 3
        if R < best[X][L]:
            best[X][L] = R
    # g[p][l] = min R over conditions with X=p, L>=l
    g = [[INF] * (n + 2) for _ in range(n + 2)]
    for p in range(1, n + 1):
        cur = INF
        row = best[p]
        gp = g[p]
        for l in range(n, 0, -1):
            if row[l] < cur:
                cur = row[l]
            gp[l] = cur
    # H[a][b] for 1<=a<=n+1, b in [a-1, n]; empty segment -> 1
    H = [[0] * (n + 2) for _ in range(n + 2)]
    for a in range(1, n + 2):
        H[a][a - 1] = 1
    inv = [0, 1] + [0] * n
    for i in range(2, n + 2):
        inv[i] = (MOD - (MOD // i) * inv[MOD % i] % MOD) % MOD
    for length in range(1, n + 1):
        ilen = inv[length]
        for l in range(1, n - length + 2):
            r = l + length - 1
            Hl = H[l]
            total = 0
            for p in range(l, r + 1):
                if g[p][l] > r:
                    total += Hl[p - 1] * H[p + 1][r]
            H[l][r] = total % MOD * ilen % MOD
    ans = H[1][n] * 1
    # h = f / n!, so f = n! * h
    fact = 1
    for i in range(2, n + 1):
        fact = fact * i % MOD
    print(ans * fact % MOD)

main()
