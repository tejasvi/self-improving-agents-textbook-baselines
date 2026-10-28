import sys

W = 9  # bytes per slot (72 bits; enough for N*p^2 < 2^72)


def matmul(A, B, n, p):
    Bp = []
    for row in B:
        bs = b''.join(x.to_bytes(W, 'little') for x in row)
        Bp.append(int.from_bytes(bs, 'little'))
    res = []
    L = W * n
    for i in range(n):
        acc = 0
        for k, a in enumerate(A[i]):
            if a:
                acc += a * Bp[k]
        bs = acc.to_bytes(L, 'little')
        res.append([int.from_bytes(bs[W * j:W * j + W], 'little') % p for j in range(n)])
    return res


def matpow(M, e, n, p):
    R = [[int(i == j) for j in range(n)] for i in range(n)]
    B = M
    while e > 0:
        if e & 1:
            R = matmul(R, B, n, p)
        e >>= 1
        if e:
            B = matmul(B, B, n, p)
    return R


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    p = int(data[1])
    vals = list(map(int, data[2:2 + n * n]))
    A = [vals[i * n:(i + 1) * n] for i in range(n)]

    if p == 2:
        B = [[v if v != 0 else 1 for v in row] for row in A]
        R = matmul(B, B, n, p)
    else:
        free = [[A[i][j] == 0 for j in range(n)] for i in range(n)]
        K = sum(sum(1 for v in row if v == 0) for row in A)
        C = [[0 if free[i][j] else A[i][j] for j in range(n)] for i in range(n)]
        R = matpow(C, p, n, p)
        for a in range(n):
            if free[a][a]:
                # T_aa = C E + E C + (p-2) E C E, supported on row a and column a
                for i in range(n):
                    R[i][a] = (R[i][a] + C[i][a]) % p
                for j in range(n):
                    R[a][j] = (R[a][j] + C[a][j]) % p
                R[a][a] = (R[a][a] + (p - 2) * C[a][a]) % p
        if p == 3:
            for a in range(n):
                for b in range(n):
                    if a != b and free[a][b]:
                        R[a][b] = (R[a][b] + C[b][a]) % p
        if K % 2 == 1:
            R = [[(-x) % p for x in row] for row in R]

    sys.stdout.write("\n".join(" ".join(str(x % p) for x in row) for row in R) + "\n")


if __name__ == "__main__":
    main()
