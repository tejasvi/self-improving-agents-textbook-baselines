import sys
from bisect import bisect_left


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    X = int(data[1])
    groups = [[], [], [], []]
    idx = 2
    for _ in range(n):
        v = int(data[idx])
        a = int(data[idx + 1])
        c = int(data[idx + 2])
        idx += 3
        groups[v].append((c, a))

    # f[v][c] = max vitamin-v amount obtainable with total calories <= c
    fs = []
    for v in (1, 2, 3):
        dp = [0] * (X + 1)
        for c, a in groups[v]:
            if c > X:
                continue
            shifted = [x + a for x in dp[:X + 1 - c]]
            dp = dp[:c] + list(map(max, dp[c:], shifted))
        fs.append(dp)

    f1, f2, f3 = fs

    def feasible(T):
        if T == 0:
            return True
        total = 0
        for f in fs:
            c = bisect_left(f, T)
            if c > X:
                return False
            total += c
            if total > X:
                return False
        return total <= X

    lo, hi = 0, min(f1[X], f2[X], f3[X])  # answer lies in [0, hi]
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    print(lo)


main()
