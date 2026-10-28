import sys


def main():
    data = sys.stdin.read().split()
    n, X = int(data[0]), int(data[1])
    groups = [[], [], [], []]
    total = [0, 0, 0, 0]
    idx = 2
    for _ in range(n):
        v = int(data[idx]); a = int(data[idx + 1]); c = int(data[idx + 2])
        idx += 3
        groups[v].append((a, c))
        total[v] += a

    # f[v][c] = max intake of vitamin v using at most c calories
    fs = []
    for v in (1, 2, 3):
        dp = [0] * (X + 1)
        for a, c in groups[v]:
            if c > X:
                continue
            shifted = [x + a for x in dp[:X + 1 - c]]
            dp[c:] = [x if x >= y else y for x, y in zip(dp[c:], shifted)]
        fs.append(dp)

    INF = X + 1

    def feasible(T):
        total_cost = 0
        for dp in fs:
            # smallest c with dp[c] >= T (dp is nondecreasing)
            if T == 0:
                g = 0
            elif dp[X] < T:
                return False
            else:
                lo, hi = 0, X
                while lo < hi:
                    mid = (lo + hi) // 2
                    if dp[mid] >= T:
                        hi = mid
                    else:
                        lo = mid + 1
                g = lo
            total_cost += g
            if total_cost > X:
                return False
        return total_cost <= X

    lo = 0
    hi = min(total[1], total[2], total[3])
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    print(lo)


main()
