import sys
from operator import mul

def main():
    data = sys.stdin.buffer.read().split()
    MOD = 998244353
    n = int(data[0]); m = int(data[1])
    INF = n + 5
    # minR[p][l]: min R over conditions with X=p and L>=l
    best = [[INF] * (n + 2) for _ in range(n + 2)]  # best[p][L]
    idx = 2
    for _ in range(m):
        L = int(data[idx]); R = int(data[idx + 1]); X = int(data[idx + 2])
        idx += 3
        if R < best[X][L]:
            best[X][L] = R
    minR = [[INF] * (n + 2) for _ in range(n + 2)]  # minR[p][l]
    for p in range(1, n + 1):
        cur = INF
        bp = best[p]
        mp = minR[p]
        for l in range(n, 0, -1):
            if bp[l] < cur:
                cur = bp[l]
            mp[l] = cur
    inv = [0, 1] + [0] * (n)
    for i in range(2, n + 2):
        inv[i] = (MOD - (MOD // i) * inv[MOD % i] % MOD) % MOD
    # B[r][p] = g(p+1, r)
    B = [[0] * (n + 2) for _ in range(n + 2)]
    for r in range(1, n + 1):
        B[r][r] = 1
    answer_g = 0
    for l in range(n, 0, -1):
        A = [0] * (n + 2)
        A[l] = 1
        # buckets: r -> list of p whose minR[p][l] == r
        bucket = [[] for _ in range(n + 2)]
        for p in range(l, n + 1):
            v = minR[p][l]
            if v <= n:
                bucket[v].append(p)
        for r in range(l, n + 1):
            for p in bucket[r]:
                A[p] = 0
            S = sum(map(mul, A[l:r + 1], B[r][l:r + 1])) % MOD
            g = S * inv[r - l + 1] % MOD
            # g(l, r) feeds A[r+1] for later same-l rows and B[r][l-1] for smaller l
            A[r + 1] = g
            B[r][l - 1] = g
            if l == 1 and r == n:
                answer_g = g
    fact = 1
    for i in range(1, n + 1):
        fact = fact * i % MOD
    print(answer_g * fact % MOD)

main()
