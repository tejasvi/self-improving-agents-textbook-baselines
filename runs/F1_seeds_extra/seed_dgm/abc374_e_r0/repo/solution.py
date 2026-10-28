import sys


def min_cost(C, a, p, b, q):
    """Minimum cost to get capacity >= C using machines (a,p) and (b,q)."""
    if C <= 0:
        return 0
    best = None
    # Optimal solution has x < b or y < a (exchange argument).
    for x in range(0, b):
        rem = C - x * a
        y = 0 if rem <= 0 else -(-rem // b)
        cost = x * p + y * q
        if best is None or cost < best:
            best = cost
        if rem <= 0:
            break
    for y in range(0, a):
        rem = C - y * b
        x = 0 if rem <= 0 else -(-rem // a)
        cost = x * p + y * q
        if cost < best:
            best = cost
        if rem <= 0:
            break
    return best


def main():
    data = sys.stdin.read().split()
    n, X = int(data[0]), int(data[1])
    procs = []
    idx = 2
    for _ in range(n):
        a, p, b, q = (int(v) for v in data[idx:idx + 4])
        idx += 4
        procs.append((a, p, b, q))

    def feasible(C):
        total = 0
        for a, p, b, q in procs:
            total += min_cost(C, a, p, b, q)
            if total > X:
                return False
        return total <= X

    lo, hi = 0, 2 * 10**9 + 10  # lo always feasible (capacity 0 costs 0)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    print(lo)


if __name__ == "__main__":
    main()
