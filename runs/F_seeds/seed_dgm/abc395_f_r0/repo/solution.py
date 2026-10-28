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
    hmax = min(U[i] + D[i] for i in range(n))

    def feasible(h):
        # U_i' must lie in [lo_i, hi_i]; D_i' = h - U_i' in [0, D_i]
        a = 0
        b = 0
        for i in range(n):
            ui = U[i]
            di = D[i]
            lo = h - di
            if lo < 0:
                lo = 0
            hi = ui if ui < h else h
            if i == 0:
                a, b = lo, hi
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
            if a > b:
                return False
        return True

    lo, hi = 0, hmax
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1

    print(total - n * lo)


main()
