import sys


def main():
    data = sys.stdin.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    K = int(data[idx]); idx += 1
    P = int(data[idx]); idx += 1
    items = []
    for _ in range(N):
        c = int(data[idx]); idx += 1
        a = [int(data[idx + j]) for j in range(K)]
        idx += K
        items.append((c, a))

    B = P + 1
    S = B ** K
    # digits of each state
    digits = []
    for s in range(S):
        d = []
        x = s
        for _ in range(K):
            d.append(x % B)
            x //= B
        digits.append(d)
    weights = [B ** j for j in range(K)]
    full = sum(P * weights[j] for j in range(K))

    INF = float("inf")
    dp = [INF] * S
    dp[0] = 0
    for c, a in items:
        new = dp[:]
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
                t += v * weights[j]
            nc = cur + c
            if nc < new[t]:
                new[t] = nc
        dp = new
    ans = dp[full]
    print(-1 if ans == INF else ans)


main()
