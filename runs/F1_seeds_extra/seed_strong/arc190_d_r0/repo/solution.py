import sys


def matmul(A, B, n, p, S, mask):
    # pack each row of B into a big integer with S-bit slots
    Bp = []
    for row in B:
        v = 0
        for j in range(n - 1, -1, -1):
            v = (v << S) | row[j]
        Bp.append(v)
    res = []
    for i in range(n):
        Ai = A[i]
        acc = 0
        for k in range(n):
            a = Ai[k]
            if a:
                acc += a * Bp[k]
        out = [0] * n
        for j in range(n):
            out[j] = ((acc >> (S * j)) & mask) % p
        res.append(out)
    return res


def matpow(M, e, n, p):
    S = 72
    mask = (1 << S) - 1
    R = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    base = M
    while e:
        if e & 1:
            R = matmul(R, base, n, p, S, mask)
        e >>= 1
        if e:
            base = matmul(base, base, n, p, S, mask)
    return R


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    p = int(data[1])
    A = []
    idx = 2
    for i in range(n):
        A.append([int(x) for x in data[idx:idx + n]])
        idx += n
    if p == 1:
        for _ in range(n):
            print(" ".join(["0"] * n))
        return
    K = sum(1 for i in range(n) for j in range(n) if A[i][j] == 0)
    sign = -1 if K % 2 else 1

    if p == 2:
        W = [[A[i][j] if A[i][j] != 0 else 1 for j in range(n)] for i in range(n)]
        W2 = matmul(W, W, n, p, 72, (1 << 72) - 1)
        res = [[(sign * W2[i][j]) % p for j in range(n)] for i in range(n)]
    else:
        M = [[A[i][j] % p for j in range(n)] for i in range(n)]
        for i in range(n):
            for j in range(n):
                if A[i][j] == 0:
                    M[i][j] = 0
        P = matpow(M, p, n, p)
        L = [[0] * n for _ in range(n)]
        for u in range(n):
            if A[u][u] == 0:
                for x in range(n):
                    if x != u:
                        L[x][u] = (L[x][u] + A[x][u]) % p
                        L[u][x] = (L[u][x] + A[u][x]) % p
        if p == 3:
            for u in range(n):
                for v in range(n):
                    if u != v and A[u][v] == 0:
                        L[u][v] = (L[u][v] + A[v][u]) % p
        res = [[(sign * (P[i][j] + L[i][j])) % p for j in range(n)] for i in range(n)]

    out = []
    for i in range(n):
        out.append(" ".join(str(x) for x in res[i]))
    sys.stdout.write("\n".join(out) + "\n")


main()
