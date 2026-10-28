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
        # Minimize p*s + q*t subject to a*s + b*t >= c, s,t >= 0 integers.
        # Exchange argument: an optimum has s < b or t < a (B units of S can be
        # swapped for A units of T with equal capacity and no more cost).
        best = None
        # Enumerate s in [0, b-1] (capped by ceil(c/a)), compute minimal t.
        for s in range(0, min(b - 1, -(-c // a)) + 1):
            rem = c - a * s
            t = -(-rem // b) if rem > 0 else 0
            cost = p * s + q * t
            if best is None or cost < best:
                best = cost
        # Enumerate t in [0, a-1] (capped by ceil(c/b)), compute minimal s.
        for t in range(0, min(a - 1, -(-c // b)) + 1):
            rem = c - b * t
            s = -(-rem // a) if rem > 0 else 0
            cost = p * s + q * t
            if best is None or cost < best:
                best = cost
        return best

    def feasible(c):
        total = 0
        for a, p, b, q in procs:
            total += min_cost(c, a, p, b, q)
            if total > x:
                return False
        return True

    # Upper bound: capacity <= max(A) * X / min(P) <= 100 * 1e7 = 1e9.
    lo, hi = 0, 2 * 10**9
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    print(lo)


main()
