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
        # Min cost to get capacity >= c using S (a,p) and T (b,q) units.
        # Optimal solution has either s < b or t < a.
        best = None
        for s in range(b):
            rem = c - s * a
            t = (rem + b - 1) // b if rem > 0 else 0
            cost = s * p + t * q
            if best is None or cost < best:
                best = cost
        for t in range(a):
            rem = c - t * b
            s = (rem + a - 1) // a if rem > 0 else 0
            cost = s * p + t * q
            if cost < best:
                best = cost
        return best

    def feasible(c):
        total = 0
        for a, p, b, q in procs:
            total += min_cost(c, a, p, b, q)
            if total > x:
                return False
        return True

    lo, hi = 0, 100 * x + 100  # lo always feasible; hi is infeasible
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid
    print(lo)


main()
