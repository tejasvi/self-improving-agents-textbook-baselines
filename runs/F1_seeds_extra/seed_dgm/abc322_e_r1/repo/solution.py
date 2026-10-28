import sys
from itertools import product


def main():
    data = sys.stdin.read().split()
    n, k, p = int(data[0]), int(data[1]), int(data[2])
    pos = 3
    items = []
    for _ in range(n):
        c = int(data[pos])
        a = [int(x) for x in data[pos + 1:pos + 1 + k]]
        pos += 1 + k
        items.append((c, a))

    states = list(product(range(p + 1), repeat=k))
    index = {s: i for i, s in enumerate(states)}
    S = len(states)
    INF = float("inf")
    dp = [INF] * S
    dp[index[tuple([0] * k)]] = 0

    for c, a in items:
        # Precompute the target state for each source state.
        trans = [index[tuple(min(p, s[j] + a[j]) for j in range(k))] for s in states]
        new = dp[:]
        for si in range(S):
            cur = dp[si]
            if cur == INF:
                continue
            ti = trans[si]
            v = cur + c
            if v < new[ti]:
                new[ti] = v
        dp = new

    goal = index[tuple([p] * k)]
    ans = dp[goal]
    print(-1 if ans == INF else ans)


main()
