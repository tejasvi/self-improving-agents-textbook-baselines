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
        # Minimum cost to reach capacity >= c using S (a,p) and T (b,q).
        # Optimal solution has either #S < b or #T < a (exchange argument),
        # so enumerating counts up to 100 for one type and greedily
        # covering the rest with the other type is exact.
        best = None
        for s in range(0, 101):
            rem = c - s * a
            t = 0 if rem <= 0 else -(-rem // b)
            cost = s * p + t * q
            if best is None or cost < best:
                best = cost
            if rem <= 0:
                break
        for t in range(0, 101):
            rem = c - t * b
            s = 0 if rem <= 0 else -(-rem // a)
            cost = s * p + t * q
            if cost < best:
                best = cost
            if rem <= 0:
                break
        return best

    def feasible(c):
        total = 0
        for a, p, b, q in procs:
            total += min_cost(c, a, p, b, q)
            if total > x:
                return False
        return True

    lo, hi = 0, 10 ** 10  # lo always feasible
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    print(lo)


main()
