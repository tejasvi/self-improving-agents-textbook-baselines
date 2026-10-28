import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    x = int(data[1])
    U = [int(v) for v in data[2:2 + 2 * n:2]]
    D = [int(v) for v in data[3:3 + 2 * n:2]]

    total = sum(U) + sum(D)
    hmax = min(u + d for u, d in zip(U, D))

    def feasible(h):
        a = b = 0
        first = True
        for i in range(n):
            u = U[i]
            d = D[i]
            lo = h - d
            if lo < 0:
                lo = 0
            hi = u if u < h else h
            if lo > hi:
                return False
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
                if na > nb:
                    return False
                a, b = na, nb
        return True

    # feasibility is monotone: if H is feasible then H-1 is feasible
    lo, hi = 0, hmax
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1

    print(total - n * lo)


main()
