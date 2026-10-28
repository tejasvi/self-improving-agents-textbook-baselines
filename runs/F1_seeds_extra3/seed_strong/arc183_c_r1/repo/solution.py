import sys
from operator import mul


def main():
    data = sys.stdin.buffer.read().split()
    MOD = 998244353
    n = int(data[0])
    m = int(data[1])
    INF = n + 5
    # byL[l] = list of (X, R) for conditions with L == l
    byL = [[] for _ in range(n + 2)]
    idx = 2
    for _ in range(m):
        L = int(data[idx])
        R = int(data[idx + 1])
        X = int(data[idx + 2])
        idx += 3
        byL[L].append((X, R))

    inv = [0, 1] + [0] * (n)
    for i in range(2, n + 2):
        inv[i] = (MOD - (MOD // i) * inv[MOD % i] % MOD) % MOD

    # col[r][p] = a[p+1][r]; col[r][r] = a[r+1][r] = 1
    col = [[0] * (n + 2) for _ in range(n + 2)]
    for r in range(1, n + 1):
        col[r][r] = 1

    T = [INF] * (n + 2)  # min R over conditions with X=p and L>=l
    a1n = 0
    for l in range(n, 0, -1):
        for (X, R) in byL[l]:
            if R < T[X]:
                T[X] = R
        # events: bucket p by T[p]
        evs = [[] for _ in range(n + 2)]
        for p in range(l, n + 1):
            if T[p] <= n:
                evs[T[p]].append(p)
        Xl = [0] * (n + 2)
        Xl[l] = 1
        for r in range(l, n + 1):
            for p in evs[r]:
                Xl[p] = 0
            s = sum(map(mul, Xl[l:r + 1], col[r][l:r + 1])) % MOD
            v = s * inv[r - l + 1] % MOD
            col[r][l - 1] = v
            Xl[r + 1] = v
            if l == 1 and r == n:
                a1n = v
    fact = 1
    for i in range(1, n + 1):
        fact = fact * i % MOD
    print(a1n * fact % MOD)


main()
