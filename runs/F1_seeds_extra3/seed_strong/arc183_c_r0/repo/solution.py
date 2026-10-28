import sys
from operator import mul
from itertools import compress

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); m = int(data[1])
    MOD = 998244353
    # best[X][R] = max L over constraints (L,R,X)
    best = [[0] * (n + 2) for _ in range(n + 2)]
    idx = 2
    for _ in range(m):
        L = int(data[idx]); R = int(data[idx + 1]); X = int(data[idx + 2])
        idx += 3
        if L > best[X][R]:
            best[X][R] = L
    # Pm[X][r] = max over R<=r of best[X][R]; interval [l,r] with root X is bad iff Pm[X][r] >= l
    Pm = [[0] * (n + 2) for _ in range(n + 2)]
    for X in range(1, n + 1):
        cur = 0
        row = best[X]
        out = Pm[X]
        for r in range(1, n + 1):
            if row[r] > cur:
                cur = row[r]
            out[r] = cur
    # Column view: PmT[r][k] = Pm[k][r]
    PmT = [[Pm[k][r] for k in range(n + 2)] for r in range(n + 2)]

    inv = [0, 1] + [0] * (n + 1)
    for i in range(2, n + 2):
        inv[i] = (MOD - (MOD // i) * inv[MOD % i] % MOD) % MOD

    # F[l][r] = D[l][r] / (r-l+1)!, with D = count for interval [l,r] (empty -> 1)
    F = [[0] * (n + 2) for _ in range(n + 3)]
    # G[r][k] = F[k][r] transposed copy for contiguous access
    G = [[0] * (n + 3) for _ in range(n + 2)]
    for l in range(1, n + 2):
        F[l][l - 1] = 1  # empty interval, length 0 -> 1
        G[l - 1][l] = 1
    for l in range(n, 0, -1):
        Fl = F[l]
        for r in range(l, n + 1):
            # k ranges over [l, r]; left = F[l][k-1] (index k-1), right = F[k+1][r] = G[r][k+1]
            Gr = G[r]
            pcol = PmT[r]
            mask = [p < l for p in pcol[l:r + 1]]
            A = Fl[l - 1:r]          # A[j] = F[l][l-1+j], k = l+j
            B = Gr[l + 1:r + 2]      # B[j] = G[r][l+1+j] = F[k+1][r], k = l+j
            s = sum(map(mul, compress(A, mask), compress(B, mask))) % MOD
            v = s * inv[r - l + 1] % MOD
            Fl[r] = v
            G[r][l] = v
    # D[1][n] = F[1][n] * n!
    ans = F[1][n]
    for i in range(1, n + 1):
        ans = ans * i % MOD
    print(ans % MOD)

main()
