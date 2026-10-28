import sys

def main():
    data = sys.stdin.buffer.read().split()
    MOD = 998244353
    N = int(data[0]); M = int(data[1])
    # best[m][r] = max L among constraints with X=m and R<=r (0 if none)
    best = [[0] * (N + 2) for _ in range(N + 2)]
    for i in range(M):
        L = int(data[2 + 3 * i]); R = int(data[3 + 3 * i]); X = int(data[4 + 3 * i])
        if L > best[X][R]:
            best[X][R] = L
    for m in range(1, N + 1):
        row = best[m]
        for r in range(1, N + 1):
            if row[r - 1] > row[r]:
                row[r] = row[r - 1]
    # bc[r][m] = best[m][r]
    bc = [[best[m][r] for m in range(N + 2)] for r in range(N + 2)]
    # a[l][r] = dp[l][r] / len!, with empty intervals = 1
    a = [[0] * (N + 2) for _ in range(N + 2)]   # a[l][r]
    at = [[0] * (N + 2) for _ in range(N + 2)]  # at[r][l] = a[l][r]
    for i in range(1, N + 2):
        a[i][i - 1] = 1
        at[i - 1][i] = 1
    inv = [0, 1] + [0] * N
    for i in range(2, N + 2):
        inv[i] = (MOD - (MOD // i) * inv[MOD % i] % MOD) % MOD
    for n in range(1, N + 1):
        for l in range(1, N - n + 2):
            r = l + n - 1
            A = a[l][l - 1:r]          # a[l][m-1], m=l..r
            B = at[r][l + 1:r + 2]     # a[m+1][r], m=l..r
            bcr = bc[r]
            s = 0
            for k in range(n):
                m = l + k
                if bcr[m] < l:
                    s += A[k] * B[k]
            h = s % MOD * inv[n] % MOD
            a[l][r] = h
            at[r][l] = h
    f = 1
    for i in range(1, N + 1):
        f = f * i % MOD
    print(f * a[1][N] % MOD)

main()
