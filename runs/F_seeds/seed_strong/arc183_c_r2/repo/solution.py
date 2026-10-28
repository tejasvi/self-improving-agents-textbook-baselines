import sys
from operator import mul

def main():
    data = sys.stdin.buffer.read().split()
    MOD = 998244353
    n = int(data[0]); m = int(data[1])
    INF = n + 1
    inv = [0, 1] + [0] * (n)
    for i in range(2, n + 1):
        inv[i] = (MOD - (MOD // i) * inv[MOD % i] % MOD) % MOD
    # best[p][L] = min R over conditions with X=p and left endpoint L
    best = [[INF] * (n + 2) for _ in range(n + 2)]
    idx = 2
    for _ in range(m):
        L = int(data[idx]); R = int(data[idx + 1]); X = int(data[idx + 2])
        idx += 3
        if R < best[X][L]:
            best[X][L] = R
    # mr[l][p] = min R over conditions with X=p, L in [l,p]
    mr = [[INF] * (n + 2) for _ in range(n + 2)]
    for p in range(1, n + 1):
        cur = INF
        bp = best[p]
        for l in range(p, 0, -1):
            if bp[l] < cur:
                cur = bp[l]
            mr[l][p] = cur
    # events[l][r] = list of p with mr[l][p] == r
    events = [[[] for _ in range(n + 2)] for _ in range(n + 2)]
    for l in range(1, n + 1):
        for p in range(l, n + 1):
            r = mr[l][p]
            if r <= n:
                events[l][r].append(p)
    # H[r][p] = g(p+1, r); g(empty)=1
    H = [[0] * (n + 2) for _ in range(n + 2)]
    for r in range(n + 1):
        H[r][r] = 1  # g(r+1, r) = 1
    g_full = 0
    for l in range(n, 0, -1):
        A = [0] * (n + 2)
        A[l] = 1  # g(l, l-1)
        for r in range(l, n + 1):
            for p in events[l][r]:
                A[p] = 0
            s = sum(map(mul, A[l:r + 1], H[r][l:r + 1])) % MOD * inv[r - l + 1] % MOD
            H[r][l - 1] = s  # g(l, r) stored as H[r][l-1]
            A[r + 1] = s
            if l == 1 and r == n:
                g_full = s
    # f(1,n) = n! * g(1,n)
    fact = 1
    for i in range(2, n + 1):
        fact = fact * i % MOD
    print(g_full * fact % MOD)

main()
