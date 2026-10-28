import sys


def main():
    data = sys.stdin.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    K = int(data[idx]); idx += 1
    P = int(data[idx]); idx += 1
    base = P + 1
    S = base ** K
    # digits[s][j] = j-th digit of state s (value of parameter j, capped at P)
    digits = []
    for s in range(S):
        d = []
        x = s
        for _ in range(K):
            d.append(x % base)
            x //= base
        digits.append(d)
    pw = [base ** j for j in range(K)]

    INF = float('inf')
    dp = [INF] * S
    dp[0] = 0
    for _ in range(N):
        C = int(data[idx]); idx += 1
        A = [int(data[idx + j]) for j in range(K)]
        idx += K
        # precompute transition target for each state
        trans = []
        for s in range(S):
            d = digits[s]
            t = 0
            for j in range(K):
                v = d[j] + A[j]
                if v > P:
                    v = P
                t += v * pw[j]
            trans.append(t)
        ndp = dp[:]
        for s in range(S):
            cur = dp[s]
            if cur == INF:
                continue
            t = trans[s]
            nc = cur + C
            if nc < ndp[t]:
                ndp[t] = nc
        dp = ndp
    target = S - 1  # all digits equal P
    ans = dp[target]
    print(-1 if ans == INF else ans)


main()
