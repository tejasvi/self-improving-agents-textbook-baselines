import sys


def matmul(X, Y, p):
    cols = list(zip(*Y))
    return [[sum(map(int.__mul__, row, col)) % p for col in cols] for row in X]


def matpow(M, e, p):
    n = len(M)
    R = [[int(i == j) for j in range(n)] for i in range(n)]
    base = M
    while e:
        if e & 1:
            R = matmul(R, base, p)
        e >>= 1
        if e:
            base = matmul(base, base, p)
    return R


def main():
    data = sys.stdin.read().split()
    n, p = int(data[0]), int(data[1])
    A = [[int(data[2 + i * n + j]) for j in range(n)] for i in range(n)]

    if p == 2:
        # Only B with zeros replaced by 1 exists (p-1 = 1).
        B = [[A[i][j] if A[i][j] != 0 else 1 for j in range(n)] for i in range(n)]
        R = matmul(B, B, p)  # B^2 mod 2
        out = [" ".join(map(str, row)) for row in R]
        sys.stdout.write("\n".join(out) + "\n")
        return

    zeros = [(i, j) for i in range(n) for j in range(n) if A[i][j] == 0]
    K = len(zeros)
    F = [[A[i][j] % p for j in range(n)] for i in range(n)]
    for i, j in zeros:
        F[i][j] = 0

    P = matpow(F, p, p)

    for a in range(n):
        if A[a][a] == 0:
            # F*E_aa: column a of F placed in column a
            for i in range(n):
                P[i][a] = (P[i][a] + F[i][a]) % p
            # E_aa*F: row a of F placed in row a
            for j in range(n):
                P[a][j] = (P[a][j] + F[a][j]) % p

    if p == 3:
        for a, b in zeros:
            if a != b:
                # E_ab F E_ab = F_ba * E_ab
                P[a][b] = (P[a][b] + F[b][a]) % p

    sign = 1 if K % 2 == 0 else p - 1
    out = []
    for row in P:
        out.append(" ".join(str(x * sign % p) for x in row))
    sys.stdout.write("\n".join(out) + "\n")


main()
