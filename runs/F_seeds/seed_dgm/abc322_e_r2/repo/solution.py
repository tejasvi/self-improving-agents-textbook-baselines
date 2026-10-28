import sys


def main():
    data = sys.stdin.read().split()
    n, k, p = int(data[0]), int(data[1]), int(data[2])
    idx = 3
    base = p + 1
    S = base ** k
    # digits of each state
    digits = []
    for s in range(S):
        d = []
        x = s
        for _ in range(k):
            d.append(x % base)
            x //= base
        digits.append(d)
    # weight of each digit position
    weights = [base ** j for j in range(k)]

    INF = float('inf')
    dp = [INF] * S
    dp[0] = 0
    for _ in range(n):
        c = int(data[idx])
        a = [int(x) for x in data[idx + 1: idx + 1 + k]]
        idx += 1 + k
        new = dp[:]
        for s in range(S):
            cur = dp[s]
            if cur == INF:
                continue
            d = digits[s]
            t = 0
            for j in range(k):
                v = d[j] + a[j]
                if v > p:
                    v = p
                t += v * weights[j]
            nc = cur + c
            if nc < new[t]:
                new[t] = nc
        dp = new
    ans = dp[S - 1]
    print(-1 if ans == INF else ans)


main()
