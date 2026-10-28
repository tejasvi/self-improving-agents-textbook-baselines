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

    def min_cost(w, a, p, b, q):
        # Minimal cost to get capacity >= w for one process.
        # Exchange argument: in an optimal solution, the count of the
        # less cost-efficient type can be bounded by 100 (the other type's
        # rate); enumerating counts 0..100 of either type suffices.
        if w <= 0:
            return 0
        best = None
        for y in range(0, 101):
            rem = w - y * b
            cost = y * q
            if rem > 0:
                cost += -(-rem // a) * p
            if best is None or cost < best:
                best = cost
            if rem <= 0:
                break
        for x in range(0, 101):
            rem = w - x * a
            cost = x * p
            if rem > 0:
                cost += -(-rem // b) * q
            if best is None or cost < best:
                best = cost
            if rem <= 0:
                break
        return best

    def feasible(w):
        total = 0
        for a, p, b, q in procs:
            total += min_cost(w, a, p, b, q)
            if total > x_budget:
                return False
        return True

    lo, hi = 0, 100 * x_budget + 1  # lo feasible, hi infeasible
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid
    print(lo)


main()
