import sys


def main():
    data = sys.stdin.read().split()
    n, X = int(data[0]), int(data[1])
    procs = []
    idx = 2
    for _ in range(n):
        a, p, b, q = (int(v) for v in data[idx:idx + 4])
        idx += 4
        procs.append((a, p, b, q))

    def min_cost(C, a, p, b, q):
        # Minimal cost to reach throughput >= C using S (a, p) and T (b, q).
        # Optimal solution exists with x < b or y < a.
        best = None
        for x in range(b):
            rem = C - a * x
            y = -(-rem // b) if rem > 0 else 0
            c = p * x + q * y
            if best is None or c < best:
                best = c
        for y in range(a):
            rem = C - b * y
            x = -(-rem // a) if rem > 0 else 0
            c = p * x + q * y
            if c < best:
                best = c
        return best

    def feasible(C):
        total = 0
        for a, p, b, q in procs:
            total += min_cost(C, a, p, b, q)
            if total > X:
                return False
        return total <= X

    lo, hi = 0, 2 * 10**9 + 10  # lo always feasible
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    print(lo)


main()
