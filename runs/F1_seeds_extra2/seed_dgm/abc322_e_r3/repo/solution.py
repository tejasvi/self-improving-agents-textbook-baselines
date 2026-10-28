import sys


def main():
    data = sys.stdin.read().split()
    n, k, p = int(data[0]), int(data[1]), int(data[2])
    idx = 3
    base = p + 1
    S = base ** k
    weights = [base ** j for j in range(k)]
    # digit[j][s] = j-th parameter value (capped at p) of state s
    digit = [[(s // weights[j]) % base for s in range(S)] for j in range(k)]
    INF = float('inf')
    dp = [INF] * S
    dp[0] = 0
    for _ in range(n):
        c = int(data[idx])
        a = [int(x) for x in data[idx + 1: idx + 1 + k]]
        idx += 1 + k
        # tbl[j][d] = contribution to target index of digit d in parameter j after adding a[j]
        tbl = [[min(d + a[j], p) * weights[j] for d in range(base)] for j in range(k)]
        new = dp[:]
        for s in range(S):
            v = dp[s]
            if v == INF:
                continue
            t = 0
            for j in range(k):
                t += tbl[j][digit[j][s]]
            nv = v + c
            if nv < new[t]:
                new[t] = nv
        dp = new
    ans = dp[S - 1]
    print(-1 if ans == INF else ans)


main()
