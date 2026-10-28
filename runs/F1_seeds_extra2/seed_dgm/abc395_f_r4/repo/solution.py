import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    x = int(data[1])
    U = [0] * n
    D = [0] * n
    for i in range(n):
        U[i] = int(data[2 + 2 * i])
        D[i] = int(data[3 + 2 * i])

    total = sum(U) + sum(D)

    def feasible(h):
        # u_i must lie in [lo_i, hi_i] where d_i = h - u_i in [0, D_i]
        a = b = None
        for i in range(n):
            lo = h - D[i]
            if lo < 0:
                lo = 0
            hi = U[i] if U[i] < h else h
            if lo > hi:
                return False
            if a is None:
                a, b = lo, hi
            else:
                na = a - x
                nb = b + x
                if na > lo:
                    lo = na
                if nb < hi:
                    hi = nb
                if lo > hi:
                    return False
                a, b = lo, hi
        return True

    lo_h = 0
    hi_h = min(U[i] + D[i] for i in range(n))
    # feasibility is monotone decreasing in h: find max feasible h
    while lo_h < hi_h:
        mid = (lo_h + hi_h + 1) // 2
        if feasible(mid):
            lo_h = mid
        else:
            hi_h = mid - 1
    print(total - n * lo_h)


main()
