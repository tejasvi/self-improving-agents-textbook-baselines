import sys


SB = 10  # bytes per slot (80 bits; max slot value N*(p-1)^2 < 2^77)


def matmul(A, B, p, N):
    # Pack each row of B into one big int (slot j = B[k][j]); then
    # row i of A*B = sum_k A[i][k] * packedRow_k, computed with scalar mults.
    Bp = [int.from_bytes(b"".join(x.to_bytes(SB, "little") for x in row), "little")
          for row in B]
    L = SB * N
    C = []
    for i in range(N):
        arow = A[i]
        S = 0
        for k in range(N):
            a = arow[k]
            if a:
                S += a * Bp[k]
        bs = S.to_bytes(L, "little")
        C.append([int.from_bytes(bs[j * SB:(j + 1) * SB], "little") % p for j in range(N)])
    return C


def mat_pow(M, e, p, N):
    R = [[1 if i == j else 0 for j in range(N)] for i in range(N)]
    B = M
    first = True
    while e:
        if e & 1:
            R = matmul(R, B, p, N)
        e >>= 1
        if e:
            B = matmul(B, B, p, N)
    return R


def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    p = int(data[1])
    vals = list(map(int, data[2:2 + N * N]))
    A = [vals[i * N:(i + 1) * N] for i in range(N)]
    if p == 2:
        M = [[x if x != 0 else 1 for x in row] for row in A]
        R = matmul(M, M, 2, N)
        print("\n".join(" ".join(map(str, row)) for row in R))
        return
    free = [[A[i][j] == 0 for j in range(N)] for i in range(N)]
    K = sum(sum(1 for x in row if x == 0) for row in A)
    A0 = [[0 if free[i][j] else A[i][j] for j in range(N)] for i in range(N)]
    total = mat_pow(A0, p, p, N)
    total = [row[:] for row in total]
    for i in range(N):
        if free[i][i]:
            # free loop at i used p-1 times, plus one fixed edge (i,t)
            for t in range(N):
                if t != i:
                    total[i][t] = (total[i][t] + A0[i][t]) % p
                    total[t][i] = (total[t][i] + A0[t][i]) % p
    if p == 3:
        for a in range(N):
            for b in range(N):
                if a != b and free[a][b]:
                    total[a][b] = (total[a][b] + A0[b][a]) % p
    if K % 2 == 1:
        total = [[(-x) % p for x in row] for row in total]
    print("\n".join(" ".join(str(x % p) for x in row) for row in total))


main()
