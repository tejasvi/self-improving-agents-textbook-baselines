import sys
from operator import mul


def mat_mul(X, Y, p):
    YT = list(zip(*Y))
    return [[sum(map(mul, row, col)) % p for col in YT] for row in X]


def mat_pow(M, e, p):
    n = len(M)
    R = [[int(i == j) for j in range(n)] for i in range(n)]
    base = M
    first = True
    while e:
        if e & 1:
            if first:
                R = base
                first = False
            else:
                R = mat_mul(R, base, p)
        e >>= 1
        if e:
            base = mat_mul(base, base, p)
    return R


def brute(N, p, A):
    # Only used for p == 2 (single matrix B) -- direct computation.
    B = [[(A[i][j] if A[i][j] != 0 else 1) for j in range(N)] for i in range(N)]
    return mat_pow(B, p, p)


def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    p = int(data[1])
    A = []
    idx = 2
    for i in range(N):
        A.append([int(x) for x in data[idx:idx + N]])
        idx += N

    if p == 2:
        res = brute(N, p, A)
    else:
        zeros = [(i, j) for i in range(N) for j in range(N) if A[i][j] == 0]
        K = len(zeros)
        # Fm: fixed entries, zero positions set to 0
        Fm = [[A[i][j] % p for j in range(N)] for i in range(N)]
        res = mat_pow(Fm, p, p)
        # Correction terms: for each zero e=(a,b), sum over walks using e p-1 times
        # and one fixed step.
        for (a, b) in zeros:
            if a == b:
                for i in range(N):
                    res[i][a] = (res[i][a] + Fm[i][a]) % p
                for j in range(N):
                    res[a][j] = (res[a][j] + Fm[a][j]) % p
                res[a][a] = (res[a][a] + (p - 2) * Fm[a][a]) % p
            elif p == 3:
                res[a][b] = (res[a][b] + Fm[b][a]) % p
        if K % 2 == 1:
            res = [[(-x) % p for x in row] for row in res]

    out = []
    for i in range(N):
        out.append(" ".join(str(x % p) for x in res[i]))
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
