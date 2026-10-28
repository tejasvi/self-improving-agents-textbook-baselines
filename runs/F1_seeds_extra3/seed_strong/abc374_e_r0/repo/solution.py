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

    def cost_of(C, a, p, b, q):
        # min cost to get capacity >= C for one process
        best = -(-C // a) * p
        t = -(-C // b) * q
        if t < best:
            best = t
        # y units of T (y < a suffices by exchange argument), rest by S
        for y in range(0, min(a - 1, -(-C // b)) + 1):
            rem = C - y * b
            c = y * q
            if rem > 0:
                c += -(-rem // a) * p
            if c < best:
                best = c
        # x units of S with x < b
        for x in range(0, min(b - 1, -(-C // a)) + 1):
            rem = C - x * a
            c = x * p
            if rem > 0:
                c += -(-rem // b) * q
            if c < best:
                best = c
        return best

    def feasible(C):
        total = 0
        for a, p, b, q in procs:
            total += cost_of(C, a, p, b, q)
            if total > X:
                return False
        return True

    lo, hi = 0, 101 * X + 1  # lo feasible, hi infeasible
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid
    print(lo)


main()
