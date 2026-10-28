import sys
import numpy as np

def main():
    data = sys.stdin.buffer.read().split()
    MOD = 998244353
    n = int(data[0]); m = int(data[1])
    arr = np.array(data[2:2 + 3 * m], dtype=np.int64).reshape(m, 3)
    Ls, Rs, Xs = arr[:, 0], arr[:, 1], arr[:, 2]
    INF = n + 5
    # H[L][X] = min R over constraints with that L and X
    H = np.full((n + 2, n + 2), INF, dtype=np.int64)
    np.minimum.at(H, (Ls, Xs), Rs)
    # G[l][p] = min R over constraints with X=p and L>=l
    G = np.minimum.accumulate(H[::-1], axis=0)[::-1].copy()

    # binomials
    C = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        C[i][0] = 1
        for j in range(1, i + 1):
            C[i][j] = (C[i - 1][j - 1] + C[i - 1][j]) % MOD
    Cn = np.array(C, dtype=np.int64)

    # F[l][r]; empty interval F[l][l-1] = 1
    F = np.zeros((n + 2, n + 2), dtype=np.int64)
    for l in range(1, n + 2):
        F[l, l - 1] = 1
    for length in range(1, n + 1):
        for l in range(1, n - length + 2):
            r = l + length - 1
            ps = slice(l, r + 1)
            allowed = G[l, l:r + 1] > r
            left = F[l, l - 1:r]
            right = F[l + 1:r + 2, r]
            c = Cn[length - 1, 0:length]
            t = (c * left) % MOD
            t = (t * right) % MOD
            t = np.where(allowed, t, 0)
            F[l, r] = int(t.sum()) % MOD
    print(int(F[1, n]) % MOD)

main()
