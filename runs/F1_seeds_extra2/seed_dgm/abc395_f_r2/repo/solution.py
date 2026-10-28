import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    x = int(data[1])
    U = [int(v) for v in data[2:2 + 2 * n:2]]
    D = [int(v) for v in data[3:3 + 2 * n:2]]
    total = sum(U) + sum(D)

    def feasible(h):
        # allowed u_i in [max(0, h-D_i), min(U_i, h)]
        a = b = None
        for i in range(n):
            L = h - D[i]
            if L < 0:
                L = 0
            R = U[i] if U[i] < h else h
            if L > R:
                return False
            if a is None:
                a, b = L, R
            else:
                a2 = a - x
                if a2 < L:
                    a2 = L
                b2 = b + x
                if b2 > R:
                    b2 = R
                if a2 > b2:
                    return False
                a, b = a2, b2
        return True

    lo = 0
    hi = min(U[i] + D[i] for i in range(n))
    # feasibility is monotone: feasible(h) implies feasible(h-1)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    print(total - n * lo)


main()
