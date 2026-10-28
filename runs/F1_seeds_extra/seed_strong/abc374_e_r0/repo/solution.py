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

    def process_cost(c, a, p, b, q):
        # Minimum cost to get sA + tB >= c. An optimal solution exists where
        # the count of the less cost-efficient type is < 100 (exchange argument).
        best = None
        # enumerate t (count of T), t <= 100
        tmax = min(-(-c // b), 100)
        for t in range(tmax + 1):
            rem = c - t * b
            s = -(-rem // a) if rem > 0 else 0
            cost = t * q + s * p
            if best is None or cost < best:
                best = cost
        # enumerate s (count of S), s <= 100
        smax = min(-(-c // a), 100)
        for s in range(smax + 1):
            rem = c - s * a
            t = -(-rem // b) if rem > 0 else 0
            cost = t * q + s * p
            if cost < best:
                best = cost
        return best

    def feasible(c):
        total = 0
        for a, p, b, q in procs:
            total += process_cost(c, a, p, b, q)
            if total > x:
                return False
        return True

    lo, hi = 0, 100 * x + 1  # hi is always infeasible
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid
    print(lo)


main()
