import sys
from operator import mul


def matmul(X, Y, p):
    # X, Y: n x n lists with entries in [0, p). Returns X*Y mod p.
    Yt = list(zip(*Y))
    return [[sum(map(mul, row, col)) % p for col in Yt] for row in X]


def matpow(M, e, p):
    n = len(M)
    R = [[int(i == j) for j in range(n)] for i in range(n)]
    B = M
    while e:
        if e & 1:
            R = matmul(R, B, p)
        e >>= 1
        if e:
            B = matmul(B, B, p)
    return R


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    p = int(data[1])
    vals = list(map(int, data[2:2 + n * n]))
    A = [vals[i * n:(i + 1) * n] for i in range(n)]

    if p == 2:
        # only one B: zeros replaced by 1; B^2 mod 2
        B = [[x if x != 0 else 1 for x in row] for row in A]
        R = matpow(B, 2, p)
    else:
        K = sum(1 for i in range(n) for j in range(n) if A[i][j] == 0)
        F = [[x for x in row] for row in A]  # zeros stay zero (only fixed-nonzero used)
        R = matpow(F, p, p)
        S = [[0] * n for _ in range(n)]
        for a in range(n):
            if A[a][a] == 0:
                # loop e=(a,a): contributes column a and row a of F
                for x in range(n):
                    S[x][a] += A[x][a]
                    S[a][x] += A[a][x]
        if p == 3:
            for a in range(n):
                for b in range(n):
                    if a != b and A[a][b] == 0:
                        S[a][b] += A[b][a]
        for i in range(n):
            for j in range(n):
                v = R[i][j] + S[i][j]
                if K % 2 == 1:
                    v = -v
                R[i][j] = v % p
    out = [" ".join(str(v % p) for v in row) for row in R]
    sys.stdout.write("\n".join(out) + "\n")


main()
