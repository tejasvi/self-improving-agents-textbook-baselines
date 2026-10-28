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
        # Minimal cost to get capacity >= c using S (a per unit, cost p) and T (b per unit, cost q).
        # Optimal solution has either s < B or t < A; enumerate those.
        best = None
        # enumerate s in [0, b-1]; t minimal
        for s in range(0, b):
            rem = c - s * a
            t = 0 if rem <= 0 else -(-rem // b)
            cost = s * p + t * q
            if best is None or cost < best:
                best = cost
            if rem <= 0:
                break
        # enumerate t in [0, a-1]; s minimal
        for t in range(0, a):
            rem = c - t * b
            s = 0 if rem <= 0 else -(-rem // a)
            cost = s * p + t * q
            if best is None or cost < best:
                best = cost
            if rem <= 0:
                break
        return best

    def feasible(c):
        if c == 0:
            return True
        total = 0
        for (a, p, b, q) in procs:
            total += min_cost(c, a, p, b, q)
            if total > x:
                return False
        return total <= x

    lo, hi = 0, 100 * x + 1  # hi is infeasible
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid
    print(lo)


main()
