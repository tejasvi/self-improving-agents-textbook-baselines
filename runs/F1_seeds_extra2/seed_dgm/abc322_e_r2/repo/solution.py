import sys
from itertools import product


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

    # Encode states as tuples of capped values (each in 0..p), mixed radix base p+1.
    base = p + 1
    size = base ** k
    weights = [base ** j for j in range(k)]
    digits = [None] * size
    for s in range(size):
        digits[s] = tuple((s // weights[j]) % base for j in range(k))

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
                v = d[j] + a[j]
                if v > p:
                    v = p
                t += v * weights[j]
            nc = cur + c
            if nc < new[t]:
                new[t] = nc
        dp = new

    target = size - 1  # all digits == p
    ans = dp[target]
    print(-1 if ans == INF else ans)


main()
