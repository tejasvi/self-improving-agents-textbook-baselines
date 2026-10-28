import sys


def main():
    data = sys.stdin.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    K = int(data[idx]); idx += 1
    P = int(data[idx]); idx += 1
    B = P + 1
    S = B ** K
    INF = float("inf")

    # digits[s] = list of per-parameter values (capped at P) for state s
    digits = []
    for s in range(S):
        d = []
        x = s
        for _ in range(K):
            d.append(x % B)
            x //= B
        digits.append(d)
    weights = [B ** j for j in range(K)]

    dp = [INF] * S
    dp[0] = 0
    for _ in range(N):
        C = int(data[idx]); idx += 1
        A = [int(data[idx + j]) for j in range(K)]
        idx += K
        ndp = dp[:]
        for s in range(S):
            cur = dp[s]
            if cur == INF:
                continue
            d = digits[s]
            t = 0
            for j in range(K):
                v = d[j] + A[j]
                if v > P:
                    v = P
                t += v * weights[j]
            nc = cur + C
            if nc < ndp[t]:
                ndp[t] = nc
        dp = ndp

    ans = dp[S - 1]
    print(-1 if ans == INF else ans)


main()
