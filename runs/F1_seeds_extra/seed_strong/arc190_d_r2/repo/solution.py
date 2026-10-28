import sys

W = 9  # bytes per slot (72 bits)


def matmul(X, Y, n, p):
    # pack rows of Y into big ints
    Yp = []
    for k in range(n):
        Yp.append(int.from_bytes(b''.join(v.to_bytes(W, 'little') for v in Y[k]), 'little'))
    L = W * n
    res = []
    for i in range(n):
        row = X[i]
        R = 0
        for k in range(n):
            a = row[k]
            if a:
                R += a * Yp[k]
        bs = R.to_bytes(L, 'little')
        res.append([int.from_bytes(bs[j * W:(j + 1) * W], 'little') % p for j in range(n)])
    return res


def matpow(M, e, n, p):
    R = [[int(i == j) for j in range(n)] for i in range(n)]
    first = True
    while e:
        if e & 1:
            R = M if first else matmul(R, M, n, p)
            first = False
        e >>= 1
        if e:
            M = matmul(M, M, n, p)
    return R


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    p = int(data[1])
    A = [[int(data[2 + i * n + j]) for j in range(n)] for i in range(n)]
    if p == 2:
        B = [[A[i][j] if A[i][j] else 1 for j in range(n)] for i in range(n)]
        # B^2 mod 2
        res = matmul(B, B, n, 2)
        out = [' '.join(map(str, row)) for row in res]
        print('\n'.join(out))
        return
    free = [[A[i][j] == 0 for j in range(n)] for i in range(n)]
    K = sum(sum(1 for v in row if v) for row in free)
    C = [[0 if free[i][j] else A[i][j] for j in range(n)] for i in range(n)]
    total = matpow(C, p, n, p)
    D = [[0] * n for _ in range(n)]
    for a in range(n):
        if free[a][a]:
            # loop e=(a,a): row a and column a contributions
            for j in range(n):
                if j != a and not free[a][j]:
                    D[a][j] += C[a][j]
                if j != a and not free[j][a]:
                    D[j][a] += C[j][a]
    if p == 3:
        for a in range(n):
            for b in range(n):
                if a != b and free[a][b]:
                    # t=1 term: U C U = C[b][a] * E_ab
                    D[a][b] += C[b][a]
    sign = 1 if K % 2 == 0 else p - 1
    out = []
    for i in range(n):
        out.append(' '.join(str(sign * ((total[i][j] + D[i][j]) % p) % p) for j in range(n)))
    print('\n'.join(out))


main()
