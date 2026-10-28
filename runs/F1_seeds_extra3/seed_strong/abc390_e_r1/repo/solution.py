import sys
from bisect import bisect_left
from itertools import repeat
from operator import add


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    X = int(data[1])
    items = [[] for _ in range(4)]
    idx = 2
    for _ in range(n):
        v = int(data[idx])
        a = int(data[idx + 1])
        c = int(data[idx + 2])
        idx += 3
        items[v].append((a, c))

    # g[v][c] = max units of vitamin v with total calories <= c
    gs = [None, None, None, None]
    for v in range(1, 4):
        dp = [0] * (X + 1)
        for a, c in items[v]:
            if c > X:
                continue
            shifted = map(add, dp[:X + 1 - c], repeat(a))
            dp = dp[:c] + list(map(max, dp[c:], shifted))
        gs[v] = dp

    def cost_for(v, m):
        # minimal calories c with g[v][c] >= m, or None
        g = gs[v]
        if m <= 0:
            return 0
        if g[X] < m:
            return None
        return bisect_left(g, m)

    def feasible(m):
        total = 0
        for v in range(1, 4):
            c = cost_for(v, m)
            if c is None:
                return False
            total += c
            if total > X:
                return False
        return total <= X

    lo, hi = 0, sum(a for v in range(1, 4) for a, _ in items[v]) + 1
    # invariant: lo feasible, hi infeasible
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid
    print(lo)


main()
