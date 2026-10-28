import sys
from operator import mul

def main():
    data = sys.stdin.buffer.read().split()
    MOD = 998244353
    n = int(data[0]); m = int(data[1])
    INF = n + 5
    # best[X][L] = min R over constraints with this X and left end L
    best = [[INF] * (n + 2) for _ in range(n + 2)]
    p = 2
    for _ in range(m):
        L = int(data[p]); R = int(data[p + 1]); X = int(data[p + 2]); p += 3
        if R < best[X][L]:
            best[X][L] = R
    # g[x][l] = min R over constraints with X=x and L>=l
    g = [[INF] * (n + 2) for _ in range(n + 2)]
    for x in range(1, n + 1):
        cur = INF
        bx = best[x]
        gx = g[x]
        for l in range(n, 0, -1):
            if bx[l] < cur:
                cur = bx[l]
            gx[l] = cur
    inv = [0, 1] + [0] * n
    for i in range(2, n + 2):
        inv[i] = (MOD - (MOD // i) * inv[MOD % i] % MOD) % MOD
    # e[l][r] = f[l][r] / len!, stored as col[r][l]; empty segments = 1
    col = [[0] * (n + 3) for _ in range(n + 3)]
    for r in range(0, n + 2):
        # col[r][r+1] = e[r+1][r] = 1 (empty)
        if r + 1 <= n + 2:
            col[r][r + 1] = 1
    for l in range(n, 0, -1):
        A = [0] * (n + 2)
        buckets = {}
        for mm in range(l, n + 1):
            t = g[mm][l]
            if t <= n:
                buckets.setdefault(t, []).append(mm)
        for r in range(l, n + 1):
            # root at r: left part e[l][r-1]
            if g[r][l] > r:
                A[r] = col[r - 1][l] if r - 1 >= l else 1
            else:
                A[r] = 0
            if r in buckets:
                for mm in buckets[r]:
                    if mm < r:
                        A[mm] = 0
            s = sum(map(mul, A[l:r + 1], col[r][l + 1:r + 2])) % MOD
            length = r - l + 1
            col[r][l] = s * inv[length] % MOD
    ans = col[n][1]
    fact = 1
    for i in range(1, n + 1):
        fact = fact * i % MOD
    print(ans * fact % MOD)

main()
