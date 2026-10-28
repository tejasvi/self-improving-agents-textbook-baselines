import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    x = int(data[1])
    U = [int(v) for v in data[2:2 + 2 * n:2]]
    D = [int(v) for v in data[3:3 + 2 * n:2]]
    total = sum(U) + sum(D)
    cap = min(u + d for u, d in zip(U, D))

    pairs = list(zip(U, D))

    def feasible(H):
        # reachable interval of U' values
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

    lo_h, hi_h = 0, cap  # lo_h always feasible
    while lo_h < hi_h:
        mid = (lo_h + hi_h + 1) // 2
        if feasible(mid):
            lo_h = mid
        else:
            hi_h = mid - 1
    print(total - n * lo_h)


main()
