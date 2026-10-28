import sys

def main():
    data = sys.stdin.buffer.read().split()
    MOD = 998244353
    n = int(data[0]); m = int(data[1])
    INF = n + 5
    # base[L][X] = min R over constraints with given L, X
    base = [[INF] * (n + 2) for _ in range(n + 2)]
    idx = 2
    for _ in range(m):
        L = int(data[idx]); R = int(data[idx + 1]); X = int(data[idx + 2])
        idx += 3
        if R < base[L][X]:
            base[L][X] = R
    # MR[l][p] = min R over constraints with X=p and L >= l
    MR = [[INF] * (n + 2) for _ in range(n + 3)]
    for l in range(n, 0, -1):
        row = MR[l]; nxt = MR[l + 1]; b = base[l]
        for p in range(1, n + 1):
            row[p] = b[p] if b[p] < nxt[p] else nxt[p]

    # rowH[l][r] = H(l,r) stored as list indexed by r; colH[r][l] indexed by l
    rowH = [[1] * (n + 2) for _ in range(n + 3)]  # empty intervals -> 1
    colH = [[1] * (n + 3) for _ in range(n + 2)]
    for length in range(1, n + 1):
        invn = pow(length, MOD - 2, MOD)
        for l in range(1, n - length + 2):
            r = l + length - 1
            mr = MR[l]
            rl = rowH[l]
            cr = colH[r]
            # p from l..r, A = H(l,p-1) = rl[p-1], B = H(p+1,r) = cr[p+1]
            s = 0
            for p in range(l, r + 1):
                if mr[p] > r:
                    s += rl[p - 1] * cr[p + 1]
            v = s % MOD * invn % MOD
            rowH[l][r] = v
            colH[r][l] = v
    fact = 1
    for i in range(1, n + 1):
        fact = fact * i % MOD
    print(rowH[1][n] * fact % MOD)

main()
