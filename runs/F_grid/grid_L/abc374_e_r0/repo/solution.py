import sys


def main():
    data = sys.stdin.read().split()
    n, x = int(data[0]), int(data[1])
    items = []
    idx = 2
    for _ in range(n):
        a, p, b, q = (int(v) for v in data[idx:idx + 4])
        idx += 4
        items.append((a, p, b, q))

    def min_cost(c, a, p, b, q):
        # Min cost to get capacity >= c using S (a per unit, cost p) and T (b per unit, cost q).
        # An optimal solution exists with t < a or s < b (exchange argument).
        best = None
        for t in range(a):
            rem = c - t * b
            s = 0 if rem <= 0 else -(-rem // a)
            cost = t * q + s * p
            if best is None or cost < best:
                best = cost
        for s in range(b):
            rem = c - s * a
            t = 0 if rem <= 0 else -(-rem // b)
            cost = s * p + t * q
            if cost < best:
                best = cost
        return best

    def feasible(c):
        total = 0
        for a, p, b, q in items:
            total += min_cost(c, a, p, b, q)
            if total > x:
                return False
        return True

    lo, hi = 0, 100 * x + 1  # feasible(lo) true, feasible(hi) false
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid
    print(lo)


main()
