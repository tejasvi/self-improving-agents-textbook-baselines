import sys


def main():
    data = sys.stdin.read().split()
    n, k, p = int(data[0]), int(data[1]), int(data[2])
    pos = 3
    items = []
    for _ in range(n):
        c = int(data[pos])
        a = [int(x) for x in data[pos + 1: pos + 1 + k]]
        pos += 1 + k
        items.append((c, a))

    base = [(p + 1) ** j for j in range(k)]
    S = (p + 1) ** k
    # digits of each state
    digits = []
    for s in range(S):
        t = s
        d = []
        for _ in range(k):
            d.append(t % (p + 1))
            t //= (p + 1)
        digits.append(d)

    INF = float('inf')
    dp = [INF] * S
    dp[0] = 0
    for c, a in items:
        # transition table for this item
        trans = [0] * S
        for s in range(S):
            d = digits[s]
            idx = 0
            for j in range(k):
                v = d[j] + a[j]
                if v > p:
                    v = p
                idx += v * base[j]
            trans[s] = idx
        ndp = dp[:]
        for s in range(S):
            v = dp[s]
            if v == INF:
                continue
            t = trans[s]
            nv = v + c
            if nv < ndp[t]:
                ndp[t] = nv
        dp = ndp

    ans = dp[S - 1]
    print(-1 if ans == INF else ans)


main()
