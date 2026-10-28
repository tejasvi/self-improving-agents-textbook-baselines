import sys

def main():
    data = sys.stdin.read().split()
    n, X = int(data[0]), int(data[1])
    procs = []
    idx = 2
    for _ in range(n):
        A, P, B, Q = (int(v) for v in data[idx:idx + 4])
        idx += 4
        procs.append((A, P, B, Q))

    def min_cost(C, A, P, B, Q):
        # min P*x + Q*y subject to A*x + B*y >= C, x,y >= 0 integers.
        # Optimal solution has x < B or y < A (exchange argument).
        best = None
        for x in range(B):
            rem = C - A * x
            y = 0 if rem <= 0 else (rem + B - 1) // B
            c = P * x + Q * y
            if best is None or c < best:
                best = c
            if rem <= 0:
                break
        for y in range(A):
            rem = C - B * y
            x = 0 if rem <= 0 else (rem + A - 1) // A
            c = P * x + Q * y
            if c < best:
                best = c
            if rem <= 0:
                break
        return best

    def feasible(C):
        total = 0
        for A, P, B, Q in procs:
            total += min_cost(C, A, P, B, Q)
            if total > X:
                return False
        return True

    lo, hi = 0, 100 * X + 1  # lo always feasible, hi infeasible
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid
    print(lo)

main()
