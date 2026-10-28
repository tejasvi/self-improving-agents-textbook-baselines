import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    X = int(data[1])
    procs = []
    idx = 2
    for _ in range(n):
        a, p, b, q = (int(v) for v in data[idx:idx + 4])
        idx += 4
        procs.append((a, p, b, q))

    def min_cost(C, a, p, b, q):
        # minimum cost to get capacity >= C for one process
        if C <= 0:
            return 0
        best = None
        if p * b <= q * a:
            # S is at least as efficient per capacity: optimal uses y < a units of T
            rng = range(0, min(a, -(-C // b)) + 1)
            for y in rng:
                rem = C - y * b
                x = -(-rem // a) if rem > 0 else 0
                c = y * q + x * p
                if best is None or c < best:
                    best = c
        else:
            # T more efficient: optimal uses x < b units of S
            rng = range(0, min(b, -(-C // a)) + 1)
            for x in rng:
                rem = C - x * a
                y = -(-rem // b) if rem > 0 else 0
                c = x * p + y * q
                if best is None or c < best:
                    best = c
        return best

    def feasible(C):
        total = 0
        for a, p, b, q in procs:
            total += min_cost(C, a, p, b, q)
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


main()
