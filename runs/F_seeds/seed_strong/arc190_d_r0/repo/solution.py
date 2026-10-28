import sys
from operator import mul


def matmul(X, Y, p):
    cols = list(zip(*Y))
    return [[sum(map(mul, row, col)) % p for col in cols] for row in X]


def matpow(M, e, p):
    n = len(M)
    R = [[int(i == j) for j in range(n)] for i in range(n)]
    B = M
    first = True
    while e:
        if e & 1:
            R = matmul(R, B, p) if not first else B
            first = False
        e >>= 1
        if e:
            B = matmul(B, B, p)
    return R


def main():
    data = sys.stdin.read().split()
    n, p = int(data[0]), int(data[1])
    vals = list(map(int, data[2:2 + n * n]))
    A = [vals[i * n:(i + 1) * n] for i in range(n)]
    free = [[A[i][j] == 0 for j in range(n)] for i in range(n)]
    K = sum(sum(r) for r in free)

    if p == 2:
        M = [[1 if free[i][j] else A[i][j] for j in range(n)] for i in range(n)]
        R = matmul(M, M, 2)
        out = [" ".join(str(x) for x in row) for row in R]
        print("\n".join(out))
        return

    F0 = [[0 if free[i][j] else A[i][j] for j in range(n)] for i in range(n)]
    ans = matpow(F0, p, p)
    T = [[0] * n for _ in range(n)]
    for i in range(n):
        if free[i][i]:
            # E_ii F0 : row i of F0 ; F0 E_ii : column i of F0
            for b in range(n):
                T[i][b] += F0[i][b]
            for a in range(n):
                T[a][i] += F0[a][i]
    if p == 3:
        # off-diagonal free (u,v): E_uv F0 E_uv = F0[v][u] E_uv
        for u in range(n):
            for v in range(n):
                if u != v and free[u][v]:
                    T[u][v] += F0[v][u]
    sign = -1 if K % 2 == 1 else 1
    out = []
    for i in range(n):
        out.append(" ".join(str((sign * (ans[i][j] + T[i][j])) % p) for j in range(n)))
    print("\n".join(out))


main()
