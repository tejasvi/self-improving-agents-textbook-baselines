import sys
from bisect import bisect_left


def main():
    data = sys.stdin.buffer.read().split()
    n, X = int(data[0]), int(data[1])
    items = [[], [], [], []]
    idx = 2
    for _ in range(n):
        v = int(data[idx]); a = int(data[idx + 1]); c = int(data[idx + 2])
        idx += 3
        items[v].append((a, c))

    # f[v][c] = max vitamin v obtainable with total calories <= c
    fs = []
    for v in (1, 2, 3):
        dp = [0] * (X + 1)
        for a, c in items[v]:
            if c > X:
                continue
            dp = dp[:c] + [x if x > y + a else y + a
                           for x, y in zip(dp[c:], dp)]
        fs.append(dp)

    def feasible(T):
        total = 0
        for f in fs:
            if T == 0:
                continue
            if f[X] < T:
                return False
            total += bisect_left(f, T)
            if total > X:
                return False
        return total <= X

    lo, hi = 0, min(fs[0][X], fs[1][X], fs[2][X])
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    print(lo)


main()
