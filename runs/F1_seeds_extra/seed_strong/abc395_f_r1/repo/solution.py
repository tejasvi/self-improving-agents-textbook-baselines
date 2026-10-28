import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    x = int(data[1])
    U = [int(v) for v in data[2:2 + 2 * n:2]]
    D = [int(v) for v in data[3:3 + 2 * n:2]]
    S = sum(U) + sum(D)
    M = min(u + d for u, d in zip(U, D))

    pairs = list(zip(U, D))

    def feasible(H):
        # reachable set of U'_i is an interval [a, b]
        a = b = None
        first = True
        for u, d in pairs:
            lo = H - d
            if lo < 0:
                lo = 0
            hi = u if u < H else H
            if first:
                a, b = lo, hi
                first = False
            else:
                na = a - x
                if na < lo:
                    na = lo
                nb = b + x
                if nb > hi:
                    nb = hi
                a, b = na, nb
            if a > b:
                return False
        return True

    lo, hi = 0, M  # feasible(lo) is True; find max feasible H
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    print(S - n * lo)


main()
