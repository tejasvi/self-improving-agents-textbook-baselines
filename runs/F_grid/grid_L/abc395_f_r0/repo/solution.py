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
    hi_bound = min(U[i] + D[i] for i in range(n))

    def feasible(H):
        # u_i must lie in [L_i, R_i]; d_i = H - u_i in [0, D_i]
        lo = None
        hi = None
        prev_lo = prev_hi = 0
        for i in range(n):
            u = U[i]
            d = D[i]
            L = H - d
            if L < 0:
                L = 0
            R = u if u < H else H
            if L > R:
                return False
            if i == 0:
                lo, hi = L, R
            else:
                lo = prev_lo - x
                if lo < L:
                    lo = L
                hi = prev_hi + x
                if hi > R:
                    hi = R
                if lo > hi:
                    return False
            prev_lo, prev_hi = lo, hi
        return True

    # feasibility is monotone in H (if H feasible then H-1 feasible)
    lo, hi = 0, hi_bound
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    print(total - n * lo)


main()
