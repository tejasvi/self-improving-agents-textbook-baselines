import sys


def main():
    data = sys.stdin.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    K = int(data[idx]); idx += 1
    P = int(data[idx]); idx += 1
    base = P + 1
    size = base ** K
    INF = float('inf')
    # Decode table: digits[s] = tuple of K parameter values (each capped at P)
    digits = []
    for s in range(size):
        t = s
        d = []
        for _ in range(K):
            d.append(t % base)
            t //= base
        digits.append(d)
    pw = [base ** j for j in range(K)]

    dp = [INF] * size
    dp[0] = 0
    for _ in range(N):
        row = data[idx:idx + 1 + K]
        idx += 1 + K
        c = int(row[0])
        a = [int(x) for x in row[1:]]
        ndp = dp[:]
        for s in range(size):
            cur = dp[s]
            if cur == INF:
                continue
            d = digits[s]
            ns = 0
            for j in range(K):
                v = d[j] + a[j]
                if v > P:
                    v = P
                ns += v * pw[j]
            nc = cur + c
            if nc < ndp[ns]:
                ndp[ns] = nc
        dp = ndp
    ans = dp[size - 1]
    print(-1 if ans == INF else ans)


main()
