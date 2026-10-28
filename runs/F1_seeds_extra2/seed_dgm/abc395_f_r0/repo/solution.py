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

    def feasible(H):
        # u_i must lie in [max(0, H - D_i), min(U_i, H)]
        lo = max(0, H - D[0])
        hi = min(U[0], H)
        if lo > hi:
            return False
        for i in range(1, n):
            a = H - D[i]
            if a < 0:
                a = 0
            b = U[i] if U[i] < H else H
            nl = lo - x
            if nl < a:
                nl = a
            nh = hi + x
            if nh > b:
                nh = b
            if nl > nh:
                return False
            lo, hi = nl, nh
        return True

    # Feasibility is monotone: if H is feasible, so is H-1.
    lo, hi = 0, hmax
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    print(total - n * lo)


main()
