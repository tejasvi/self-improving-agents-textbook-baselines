import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    x = int(data[1])
    U = [int(v) for v in data[2::2][:n]]
    D = [int(v) for v in data[3::2][:n]]
    S = [U[i] + D[i] for i in range(n)]
    total = sum(S)
    min_s = min(S)

    def feasible(h):
        # Reachable set for upper tooth i is an interval [lo, hi].
        lo = hi = None
        for i in range(n):
            u = U[i]
            d = D[i]
            L = h - d
            if L < 0:
                L = 0
            R = u if u < h else h
            if L > R:
                return False
            if lo is None:
                lo, hi = L, R
            else:
                lo -= x
                hi += x
                if lo < L:
                    lo = L
                if hi > R:
                    hi = R
                if lo > hi:
                    return False
        return True

    # Feasibility is monotone: if H is feasible, so is H-1.
    lo, hi = 0, min_s
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    print(total - n * lo)


main()
