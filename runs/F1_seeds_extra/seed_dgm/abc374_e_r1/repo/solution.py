import sys


def main():
    data = sys.stdin.read().split()
    n, x = int(data[0]), int(data[1])
    procs = []
    idx = 2
    for _ in range(n):
        a, p, b, q = (int(v) for v in data[idx:idx + 4])
        idx += 4
        procs.append((a, p, b, q))

    def min_cost(c, a, p, b, q):
        # Minimum cost to reach throughput >= c using machines S(a,p) and T(b,q).
        # Exchange argument: the count of the worse-ratio machine can be
        # assumed < rate of the better one (<= 100), so enumerate it.
        best = None
        for (r1, c1, r2, c2) in ((a, p, b, q), (b, q, a, p)):
            for k in range(0, 101):
                rem = c - k * r1
                if rem < 0:
                    rem = 0
                cost = k * c1 + (-(-rem // r2)) * c2
                if best is None or cost < best:
                    best = cost
                if rem == 0:
                    break
        return best

    def feasible(c):
        total = 0
        for a, p, b, q in procs:
            total += min_cost(c, a, p, b, q)
            if total > x:
                return False
        return total <= x

    lo, hi = 0, 2 * 10**9  # lo always feasible
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    print(lo)


main()
