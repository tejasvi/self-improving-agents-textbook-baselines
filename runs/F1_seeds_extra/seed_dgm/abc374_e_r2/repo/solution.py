import sys


def cost_for(C, A, P, B, Q):
    """Minimum cost to get capacity >= C from one process."""
    if C <= 0:
        return 0
    best = None
    # Optimal solution can be chosen with y < A (T count) or x < B (S count),
    # by exchanging A units of T with B units of S (same capacity A*B).
    for y in range(0, A):
        rem = C - B * y
        x = 0 if rem <= 0 else -(-rem // A)
        c = P * x + Q * y
        if best is None or c < best:
            best = c
        if rem <= 0:
            break
    for x in range(0, B):
        rem = C - A * x
        y = 0 if rem <= 0 else -(-rem // B)
        c = P * x + Q * y
        if best is None or c < best:
            best = c
        if rem <= 0:
            break
    return best


def main():
    data = sys.stdin.read().split()
    n, X = int(data[0]), int(data[1])
    items = []
    idx = 2
    for _ in range(n):
        A, P, B, Q = (int(v) for v in data[idx:idx + 4])
        idx += 4
        items.append((A, P, B, Q))

    def feasible(C):
        total = 0
        for A, P, B, Q in items:
            total += cost_for(C, A, P, B, Q)
            if total > X:
                return False
        return True

    lo, hi = 0, 2 * 10**9 + 1  # lo always feasible; hi infeasible
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid
    print(lo)


if __name__ == "__main__":
    main()
