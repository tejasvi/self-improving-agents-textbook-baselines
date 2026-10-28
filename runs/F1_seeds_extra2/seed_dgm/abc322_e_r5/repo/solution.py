import sys


def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    k = int(data[idx]); idx += 1
    p = int(data[idx]); idx += 1
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
    # power weights for encoding
    weights = [base ** j for j in range(k)]
    INF = float('inf')
    dp = [INF] * S
    dp[0] = 0
    for _ in range(n):
        c = int(data[idx]); idx += 1
        a = [int(data[idx + j]) for j in range(k)]
        idx += k
        trans = [0] * S
        for s in range(S):
            d = digits[s]
            t = 0
            for j in range(k):
                v = d[j] + a[j]
                if v > p:
                    v = p
                t += v * weights[j]
            trans[s] = t
        new = dp[:]
        for s in range(S):
            cur = dp[s]
            if cur == INF:
                continue
            nt = trans[s]
            nc = cur + c
            if nc < new[nt]:
                new[nt] = nc
        dp = new
    ans = dp[S - 1]
    print(-1 if ans == INF else ans)


main()
