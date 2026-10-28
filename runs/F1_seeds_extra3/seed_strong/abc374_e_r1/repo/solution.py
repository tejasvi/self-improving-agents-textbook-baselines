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

    def cost(c, a, p, b, q):
        # min s*p + t*q  s.t. s*a + t*b >= c, s,t >= 0 integers.
        # Exchange argument: an optimum exists with t < a or s < b.
        best = None
        tmax = min(a - 1, -(-c // b))
        for t in range(tmax + 1):
            rem = c - t * b
            s = -(-rem // a) if rem > 0 else 0
            v = t * q + s * p
            if best is None or v < best:
                best = v
        smax = min(b - 1, -(-c // a))
        for s in range(smax + 1):
            rem = c - s * a
            t = -(-rem // b) if rem > 0 else 0
            v = t * q + s * p
            if best is None or v < best:
                best = v
        return best

    def feasible(c):
        total = 0
        for a, p, b, q in procs:
            total += cost(c, a, p, b, q)
            if total > x:
                return False
        return True

    lo, hi = 0, 100 * x + 100  # lo always feasible
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    print(lo)


main()
