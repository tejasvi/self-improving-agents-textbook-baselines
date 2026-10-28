import sys


def main():
    data = sys.stdin.read().split()
    n, k, p = int(data[0]), int(data[1]), int(data[2])
    idx = 3
    plans = []
    for _ in range(n):
        c = int(data[idx])
        a = [int(x) for x in data[idx + 1: idx + 1 + k]]
        idx += 1 + k
        plans.append((c, a))

    base = p + 1
    size = base ** k
    # Decode each state into its digit vector (parameter values capped at p).
    digits = []
    for s in range(size):
        v = []
        t = s
        for _ in range(k):
            v.append(t % base)
            t //= base
        digits.append(v)
    weights = [base ** j for j in range(k)]

    INF = float("inf")
    dp = [INF] * size
    dp[0] = 0
    for c, a in plans:
        new = dp[:]
        for s in range(size):
            cur = dp[s]
            if cur == INF:
                continue
            d = digits[s]
            t = 0
            for j in range(k):
                x = d[j] + a[j]
                if x > p:
                    x = p
                t += x * weights[j]
            nc = cur + c
            if nc < new[t]:
                new[t] = nc
        dp = new

    target = size - 1  # all digits equal to p
    ans = dp[target]
    print(-1 if ans == INF else ans)


main()
