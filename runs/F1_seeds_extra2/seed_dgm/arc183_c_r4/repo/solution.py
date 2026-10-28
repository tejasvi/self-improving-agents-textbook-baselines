import sys
import numpy as np

def main():
    MOD = 998244353
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    arr = np.array(data[2:2 + 3 * m], dtype=np.int64).reshape(m, 3)
    Ls, Rs, Xs = arr[:, 0], arr[:, 1], arr[:, 2]
    INF = n + 5
    # best[L][X] = min R over conditions with that L and X
    best = np.full((n + 2, n + 2), INF, dtype=np.int64)
    np.minimum.at(best, (Ls, Xs), Rs)
    # G[l][p] = min R over conditions with X=p and L>=l
    G = np.minimum.accumulate(best[::-1], axis=0)[::-1]

    # binomials
    C = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        C[i][0] = 1
        for j in range(1, i + 1):
            C[i][j] = (C[i - 1][j - 1] + C[i - 1][j]) % MOD
    Cnp = np.array(C, dtype=np.int64)

    F = np.zeros((n + 2, n + 2), dtype=np.int64)
    for l in range(1, n + 2):
        F[l][l - 1] = 1
    for length in range(1, n + 1):
        for l in range(1, n - length + 2):
            r = l + length - 1
            ps = np.arange(l, r + 1)
            valid = G[l, l:r + 1] > r
            left = F[l, l - 1:r]           # F[l][p-1]
            right = F[l + 1:r + 2, r]      # F[p+1][r]
            binom = Cnp[length - 1, 0:length]
            t = binom * left % MOD * right % MOD
            t = t * valid
            F[l, r] = int(t.sum() % MOD)
    print(int(F[1, n]) % MOD)

main()
