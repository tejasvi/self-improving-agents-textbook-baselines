import sys
from operator import mul

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
    # mr[l][p] = min R over conditions with X=p, L>=l
    mr = [[INF] * (n + 2) for _ in range(n + 2)]
    for p in range(1, n + 1):
        cur = INF
        for l in range(n, 0, -1):
            if best[p][l] < cur:
                cur = best[p][l]
            mr[l][p] = cur

    fact = [1] * (n + 2)
    for i in range(1, n + 2):
        fact[i] = fact[i - 1] * i % MOD
    inv = [0, 1] + [0] * (n + 1)
    for i in range(2, n + 2):
        inv[i] = (MOD - (MOD // i) * inv[MOD % i] % MOD) % MOD

    # colH[r][k] = h[k][r] for k<=r, and colH[r][r+1] = 1
    colH = [[0] * (n + 3) for _ in range(n + 2)]
    for r in range(0, n + 1):
        colH[r][r + 1] = 1
    h_full = 0
    for l in range(n, 0, -1):
        # A[p] = h[l][p-1] if valid for current r, else 0; A[l] = 1 (empty)
        A = [0] * (n + 2)
        A[l] = 1
        buckets = [[] for _ in range(n + 2)]
        mrl = mr[l]
        for p in range(l, n + 1):
            t = mrl[p]
            if t <= n:
                buckets[t].append(p)
        for r in range(l, n + 1):
            for p in buckets[r]:
                A[p] = 0
            s = sum(map(mul, A[l:r + 1], colH[r][l + 1:r + 2])) % MOD
            hv = s * inv[r - l + 1] % MOD
            colH[r][l] = hv
            A[r + 1] = hv
            if l == 1 and r == n:
                h_full = hv
    ans = h_full * fact[n] % MOD
    print(ans)

main()
