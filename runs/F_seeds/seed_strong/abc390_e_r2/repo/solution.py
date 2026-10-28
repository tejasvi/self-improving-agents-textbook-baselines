import sys
from bisect import bisect_left


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    X = int(data[1])
    groups = [[], [], [], []]
    idx = 2
    for _ in range(n):
        v = int(data[idx]); a = int(data[idx + 1]); c = int(data[idx + 2])
        idx += 3
        groups[v].append((c, a))

    # f[v][c] = max total of vitamin v using calories <= c
    fs = []
    for v in (1, 2, 3):
        # prune: for each cost c, only the top X//c items by amount can matter
        by_cost = {}
        for c, a in groups[v]:
            by_cost.setdefault(c, []).append(a)
        items = []
        for c, lst in by_cost.items():
            lst.sort(reverse=True)
            for a in lst[: X // c]:
                items.append((c, a))
        dp = [0] * (X + 1)
        for c, a in items:
            # 0/1 knapsack step: new[j] = max(dp[j], dp[j-c] + a) for j >= c
            prev = dp[: X + 1 - c]
            cur = dp[c:]
            dp[c:] = [q + a if q + a > p else p for p, q in zip(cur, prev)]
        fs.append(dp)

    hi = 0
    for v in (1, 2, 3):
        hi = max(hi, sum(a for _, a in groups[v]))

    def feasible(T):
        if T == 0:
            return True
        s = 0
        for dp in fs:
            c = bisect_left(dp, T)
            if c > X:
                return False
            s += c
            if s > X:
                return False
        return s <= X

    lo = 0  # feasible
    hi += 1  # infeasible
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid
    print(lo)


main()
