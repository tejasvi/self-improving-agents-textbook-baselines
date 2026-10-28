import sys


def main():
    data = sys.stdin.read().split()
    n, budget = int(data[0]), int(data[1])
    procs = []
    idx = 2
    for _ in range(n):
        a, p, b, q = (int(v) for v in data[idx:idx + 4])
        idx += 4
        procs.append((a, p, b, q))

    def min_cost(C, a, p, b, q):
        # minimal cost of x*S + y*T with a*x + b*y >= C, x,y >= 0 integers
        if C <= 0:
            return 0
        best = None
        # optimal solution has y < a or x < b (exchange argument)
        for y in range(a):
            rem = C - b * y
            x = 0 if rem <= 0 else -(-rem // a)
            cost = p * x + q * y
            if best is None or cost < best:
                best = cost
            if rem <= 0:
                break
        for x in range(b):
            rem = C - a * x
            y = 0 if rem <= 0 else -(-rem // b)
            cost = p * x + q * y
            if best is None or cost < best:
                best = cost
            if rem <= 0:
                break
        return best

    def feasible(C):
        total = 0
        for a, p, b, q in procs:
            total += min_cost(C, a, p, b, q)
            if total > budget:
                return False
        return True

    lo, hi = 0, 2 * 10**9 + 10  # hi is infeasible
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid
    print(lo)


main()
