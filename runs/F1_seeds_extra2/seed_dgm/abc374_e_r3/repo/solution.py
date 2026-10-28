import sys


def main():
    data = sys.stdin.read().split()
    n, x = int(data[0]), int(data[1])
    procs = []
    idx = 2
    for _ in range(n):
        a, p, b, q = map(int, data[idx:idx + 4])
        idx += 4
        # order machines so that machine g has cost-per-capacity no worse than w
        if p * b <= q * a:
            procs.append((a, p, b, q))  # g = S, w = T
        else:
            procs.append((b, q, a, p))  # g = T, w = S

    def min_cost(c, rg, cg, rw, cw):
        # Optimal solution uses fewer than rg (<=100) units of the worse machine,
        # so enumerate that count (plus the pure-worse solution when small).
        best = None
        kmax = min((c + rw - 1) // rw, 100)
        for k in range(kmax + 1):
            rem = c - k * rw
            g = 0 if rem <= 0 else (rem + rg - 1) // rg
            cost = k * cw + g * cg
            if best is None or cost < best:
                best = cost
        return best

    def feasible(c):
        if c <= 0:
            return True
        total = 0
        for rg, cg, rw, cw in procs:
            total += min_cost(c, rg, cg, rw, cw)
            if total > x:
                return False
        return total <= x

    lo, hi = 0, 2 * 10**9
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    print(lo)


main()
