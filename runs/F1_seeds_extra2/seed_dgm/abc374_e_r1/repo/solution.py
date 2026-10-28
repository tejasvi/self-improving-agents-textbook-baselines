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

    def cost_for(C):
        # minimal cost for process to reach capacity >= C, or None if impossible
        # (impossible never happens: buying machines always works)
        total = 0
        for A, P, B, Q in procs:
            if C <= 0:
                continue
            best = None
            # enumerate number of S machines x in [0, B-1] (and up to needed)
            maxx = min(B - 1, -(-C // A))
            for x in range(maxx + 1):
                rem = C - x * A
                y = -(-rem // B) if rem > 0 else 0
                c = x * P + y * Q
                if best is None or c < best:
                    best = c
            # enumerate number of T machines y in [0, A-1]
            maxy = min(A - 1, -(-C // B))
            for y in range(maxy + 1):
                rem = C - y * B
                x = -(-rem // A) if rem > 0 else 0
                c = x * P + y * Q
                if best is None or c < best:
                    best = c
            total += best
            if total > X:
                return total
        return total

    lo, hi = 0, 100 * X + 1  # lo always feasible; hi infeasible
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if cost_for(mid) <= X:
            lo = mid
        else:
            hi = mid
    print(lo)


main()
