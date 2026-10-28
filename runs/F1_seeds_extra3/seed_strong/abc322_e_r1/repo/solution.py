import sys


def main():
    data = sys.stdin.read().split()
    n, k, p = int(data[0]), int(data[1]), int(data[2])
    base = p + 1
    S = base ** k
    weights = [base ** j for j in range(k)]
    # digit tables: digs[j][s] = digit j of state s
    digs = [[(s // weights[j]) % base for s in range(S)] for j in range(k)]
    INF = float('inf')
    dp = [INF] * S
    dp[0] = 0
    pos = 3
    for _ in range(n):
        c = int(data[pos])
        a = [int(x) for x in data[pos + 1:pos + 1 + k]]
        pos += 1 + k
        # per-parameter lookup: contribution of digit d after adding a_j, capped at p
        tabs = [[min(d + a[j], p) * weights[j] for d in range(base)] for j in range(k)]
        new = dp[:]
        for s in range(S):
            v = dp[s]
            if v == INF:
                continue
            t = 0
            for j in range(k):
                t += tabs[j][digs[j][s]]
            nv = v + c
            if nv < new[t]:
                new[t] = nv
        dp = new
    ans = dp[S - 1]
    print(-1 if ans == INF else ans)


main()
