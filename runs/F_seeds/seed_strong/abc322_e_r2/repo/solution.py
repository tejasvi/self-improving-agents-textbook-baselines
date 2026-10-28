import sys


def main():
    data = sys.stdin.read().split()
    n, k, p = int(data[0]), int(data[1]), int(data[2])
    base = p + 1
    S = base ** k
    # digit tuples for each state (state encodes parameter values in base p+1)
    digits = []
    for s in range(S):
        d = []
        x = s
        for _ in range(k):
            d.append(x % base)
            x //= base
        digits.append(d)
    weights = [base ** j for j in range(k)]
    INF = float('inf')
    dp = [INF] * S
    dp[0] = 0
    pos = 3
    for _ in range(n):
        c = int(data[pos])
        a = [int(x) for x in data[pos + 1:pos + 1 + k]]
        pos += 1 + k
        new = dp[:]
        for s in range(S):
            v = dp[s]
            if v == INF:
                continue
            d = digits[s]
            t = 0
            for j in range(k):
                x = d[j] + a[j]
                if x > p:
                    x = p
                t += x * weights[j]
            nv = v + c
            if nv < new[t]:
                new[t] = nv
        dp = new
    ans = dp[S - 1]
    print(ans if ans != INF else -1)


main()
