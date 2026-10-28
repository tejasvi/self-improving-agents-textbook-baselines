import sys

MOD = 998244353

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); m = int(data[1])
    INF = n + 5
    # best[L][X] = min R over constraints with this L and X
    best = [[INF] * (n + 2) for _ in range(n + 2)]
    idx = 2
    for _ in range(m):
        L = int(data[idx]); R = int(data[idx + 1]); X = int(data[idx + 2])
        idx += 3
        if R < best[L][X]:
            best[L][X] = R
    # g[l][X] = min over L >= l of best[L][X]; a segment [l,r] with max at X
    # is invalid iff r >= g[l][X].
    g = [[INF] * (n + 2) for _ in range(n + 3)]
    for l in range(n, 0, -1):
        row = g[l]; nxt = g[l + 1]; b = best[l]
        for x in range(n + 2):
            v = nxt[x]
            if b[x] < v:
                v = b[x]
            row[x] = v

    inv = [0, 1] + [0] * (n + 1)
    for i in range(2, n + 2):
        inv[i] = (MOD - (MOD // i) * inv[MOD % i] % MOD) % MOD

    # A[l][r] = f(l,r) / (r-l+1)!, with f of empty segment = 1.
    # A[x][x-1] = 1 for all x.
    A = [[0] * (n + 2) for _ in range(n + 3)]
    for x in range(1, n + 3):
        if x - 1 <= n + 1:
            A[x][x - 1] = 1
    for l in range(n, 0, -1):
        Al = A[l]
        acc = [0] * (n + 2)
        Al[l - 1] = 1
        for p in range(l, n + 1):
            c = Al[p - 1]
            if c:
                hi = min(n, g[l][p] - 1)
                if hi >= p:
                    Ap1 = A[p + 1]
                    acc[p:hi + 1] = [x + c * y for x, y in
                                     zip(acc[p:hi + 1], Ap1[p:hi + 1])]
            Al[p] = acc[p] % MOD * inv[p - l + 1] % MOD
    fact = 1
    for i in range(2, n + 1):
        fact = fact * i % MOD
    print(A[1][n] * fact % MOD)

main()
