import sys


def matmul(X, Y, n):
    # X, Y: lists of lists of ints (python bigints, reduced later)
    Yt = list(zip(*Y))
    return [[sum(map(int.__mul__, row, col)) for col in Yt] for row in X]


def matmod(X, Y, p, n):
    Yt = list(zip(*Y))
    return [[sum(map(int.__mul__, row, col)) % p for col in Yt] for row in X]


def matpow(M, e, p, n):
    R = [[int(i == j) for j in range(n)] for i in range(n)]
    B = [[v % p for v in row] for row in M]
    while e:
        if e & 1:
            R = matmod(R, B, p, n)
        e >>= 1
        if e:
            B = matmod(B, B, p, n)
    return R


def main():
    data = sys.stdin.read().split()
    n, p = int(data[0]), int(data[1])
    vals = [int(x) for x in data[2:2 + n * n]]
    A = [vals[i * n:(i + 1) * n] for i in range(n)]

    if p == 2:
        B = [[v if v != 0 else 1 for v in row] for row in A]
        R = matmod(B, B, p, n)
    else:
        K = sum(1 for row in A for v in row if v == 0)
        F = [row[:] for row in A]  # free cells (zeros) stay zero
        R = matpow(F, p, p, n)
        # free diagonal cell (a,a): adds F*E_aa + E_aa*F
        for a in range(n):
            if A[a][a] == 0:
                for i in range(n):
                    R[i][a] = (R[i][a] + F[i][a]) % p
                for j in range(n):
                    R[a][j] = (R[a][j] + F[a][j]) % p
        if p == 3:
            # free off-diagonal cell (a,b): adds F[b][a] at (a,b)
            for a in range(n):
                for b in range(n):
                    if a != b and A[a][b] == 0:
                        R[a][b] = (R[a][b] + F[b][a]) % p
        if K % 2 == 1:
            R = [[(-v) % p for v in row] for row in R]

    out = []
    for i in range(n):
        out.append(" ".join(str(v % p) for v in R[i]))
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
