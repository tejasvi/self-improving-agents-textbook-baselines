import sys


def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    k = int(data[idx]); idx += 1
    p = int(data[idx]); idx += 1
    items = []
    for _ in range(n):
        c = int(data[idx]); idx += 1
        a = [int(x) for x in data[idx:idx + k]]
        idx += k
        items.append((c, a))

    base = p + 1
    total = base ** k
    # digits of each state
    digits = []
    for s in range(total):
        d = []
        t = s
        for _ in range(k):
            d.append(t % base)
            t //= base
        digits.append(d)
    weights = [base ** j for j in range(k)]

    INF = float('inf')
    dp = [INF] * total
    dp[0] = 0
    for c, a in items:
        new = dp[:]
        for s in range(total):
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

    full = total - 1  # all digits equal to p
    ans = dp[full]
    print(-1 if ans == INF else ans)


if __name__ == "__main__":
    main()
