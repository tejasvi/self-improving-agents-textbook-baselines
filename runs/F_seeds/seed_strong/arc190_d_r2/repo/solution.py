import sys


def matmul(A, B, p):
    n = len(A)
    W = 80  # slot width in bits; entries < 2^30, products sum < 2^67
    mask = (1 << W) - 1
    # pack rows of B
    packed = []
    for k in range(n):
        v = 0
        row = B[k]
        for j in range(n - 1, -1, -1):
            v = (v << W) | row[j]
        packed.append(v)
    C = []
    for i in range(n):
        ai = A[i]
        acc = 0
        for k in range(n):
            a = ai[k]
            if a:
                acc += a * packed[k]
        out = [0] * n
        for j in range(n):
            out[j] = ((acc >> (W * j)) & mask) % p
        C.append(out)
    return C


def matpow(M, e, p):
    n = len(M)
    R = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    B = [[x % p for x in row] for row in M]
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
    A = [[int(data[2 + i * n + j]) for j in range(n)] for i in range(n)]

    if p == 2:
        M = [[A[i][j] if A[i][j] != 0 else 1 for j in range(n)] for i in range(n)]
        R = matpow(M, 2, p)
    else:
        zeros = [(i, j) for i in range(n) for j in range(n) if A[i][j] == 0]
        K = len(zeros)
        Af = [row[:] for row in A]
        R = matpow(Af, p, p)
        C = [[0] * n for _ in range(n)]
        # zero loops at a: walks a^{p-1} g or g a^{p-1}
        for a in range(n):
            if A[a][a] != 0:
                continue
            for v in range(n):
                if v == a:
                    continue
                C[a][v] += A[a][v]
                C[v][a] += A[v][a]
        if p == 3:
            # walk a,b,a,b with zero edge e=(a,b) (a!=b) used twice and g=(b,a)
            for (a, b) in zeros:
                if a != b:
                    C[a][b] += A[b][a]
        for i in range(n):
            for j in range(n):
                R[i][j] = (R[i][j] + C[i][j]) % p
        if K % 2 == 1:
            for i in range(n):
                for j in range(n):
                    R[i][j] = (-R[i][j]) % p

    out = []
    for i in range(n):
        out.append(" ".join(str(x % p) for x in R[i]))
    sys.stdout.write("\n".join(out) + "\n")


main()
