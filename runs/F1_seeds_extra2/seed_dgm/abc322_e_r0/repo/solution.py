import sys
import itertools


def main():
    data = sys.stdin.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    K = int(data[idx]); idx += 1
    P = int(data[idx]); idx += 1
    plans = []
    for _ in range(N):
        c = int(data[idx]); idx += 1
        a = [int(x) for x in data[idx:idx + K]]
        idx += K
        plans.append((c, a))

    B = P + 1
    S = B ** K
    INF = float('inf')
    # digits[s][j] = value of parameter j in state s (capped at P)
    digits = []
    for s in range(S):
        d = []
        x = s
        for _ in range(K):
            d.append(x % B)
            x //= B
        digits.append(d)
    pw = [B ** j for j in range(K)]

    dp = [INF] * S
    dp[0] = 0
    for c, a in plans:
        ndp = dp[:]
        for s in range(S):
            cur = dp[s]
            if cur == INF:
                continue
            d = digits[s]
            t = 0
            for j in range(K):
                v = d[j] + a[j]
                if v > P:
                    v = P
                t += v * pw[j]
            nv = cur + c
            if nv < ndp[t]:
                ndp[t] = nv
        dp = ndp

    ans = dp[S - 1]  # all parameters at P (digits all equal P)
    print(-1 if ans == INF else ans)


main()
