import sys


def min_cost(C, A, P, B, Q):
    # min xP + yQ subject to xA + yB >= C, x,y >= 0 integers.
    # WLOG optimal has y < A or x < B (exchange argument).
    if C <= 0:
        return 0
    best = None
    for y in range(A):
        rem = C - y * B
        x = 0 if rem <= 0 else -(-rem // A)
        c = x * P + y * Q
        if best is None or c < best:
            best = c
    for x in range(B):
        rem = C - x * A
        y = 0 if rem <= 0 else -(-rem // B)
        c = x * P + y * Q
        if c < best:
            best = c
    return best


def main():
    data = sys.stdin.read().split()
    n, X = int(data[0]), int(data[1])
    procs = []
    idx = 2
    for _ in range(n):
        A, P, B, Q = (int(v) for v in data[idx:idx + 4])
        idx += 4
        procs.append((A, P, B, Q))

    def feasible(C):
        total = 0
        for A, P, B, Q in procs:
            total += min_cost(C, A, P, B, Q)
            if total > X:
                return False
        return True

    lo, hi = 0, 100 * X + 1  # lo feasible, hi infeasible
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid
    print(lo)


main()
