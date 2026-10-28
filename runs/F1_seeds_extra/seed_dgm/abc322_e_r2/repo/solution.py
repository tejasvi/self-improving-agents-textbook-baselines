import sys

def main():
    data = sys.stdin.read().split()
    n, k, p = int(data[0]), int(data[1]), int(data[2])
    idx = 3
    base = p + 1
    total = base ** k
    # decode digits for each state
    digits = []
    for s in range(total):
        d = []
        t = s
        for _ in range(k):
            d.append(t % base)
            t //= base
        digits.append(d)
    INF = float('inf')
    dp = [INF] * total
    dp[0] = 0
    pw = [base ** j for j in range(k)]
    for _ in range(n):
        c = int(data[idx]); idx += 1
        a = [int(x) for x in data[idx:idx + k]]; idx += k
        ndp = dp[:]
        for s in range(total):
            cur = dp[s]
            if cur == INF:
                continue
            d = digits[s]
            ns = 0
            for j in range(k):
                v = d[j] + a[j]
                if v > p:
                    v = p
                ns += v * pw[j]
            nc = cur + c
            if nc < ndp[ns]:
                ndp[ns] = nc
        dp = ndp
    target = total - 1  # all digits equal to p
    ans = dp[target]
    print(-1 if ans == INF else ans)

main()
