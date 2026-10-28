import sys


def main():
    data = sys.stdin.read().split()
    n, x_budget = int(data[0]), int(data[1])
    procs = []
    idx = 2
    for _ in range(n):
        a, p, b, q = (int(v) for v in data[idx:idx + 4])
        idx += 4
        procs.append((a, p, b, q))

    def cost_for(c, a, p, b, q):
        # Minimum cost to get capacity >= c using machines S (a, p) and T (b, q).
        # Exchange argument: if b*p >= a*q, some optimal solution uses x < b
        # units of S; otherwise some optimal solution uses y < a units of T.
        if c <= 0:
            return 0
        best = None
        if b * p >= a * q:
            maxx = min(b - 1, (c + a - 1) // a)
            for x in range(maxx + 1):
                rem = c - x * a
                y = (rem + b - 1) // b if rem > 0 else 0
                cost = x * p + y * q
                if best is None or cost < best:
                    best = cost
        else:
            maxy = min(a - 1, (c + b - 1) // b)
            for y in range(maxy + 1):
                rem = c - y * b
                x = (rem + a - 1) // a if rem > 0 else 0
                cost = x * p + y * q
                if best is None or cost < best:
                    best = cost
        return best

    def feasible(c):
        total = 0
        for a, p, b, q in procs:
            total += cost_for(c, a, p, b, q)
            if total > x_budget:
                return False
        return total <= x_budget

    lo, hi = 0, 10 ** 10  # lo always feasible, hi infeasible
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid
    print(lo)


main()
