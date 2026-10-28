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

    def feasible(h):
        # Need U'_i in [max(0, h-D_i), min(U_i, h)], |U'_i - U'_{i+1}| <= x
        a = max(0, h - D[0])
        b = min(U[0], h)
        if a > b:
            return False
        for i in range(1, n):
            L = h - D[i]
            if L < 0:
                L = 0
            R = U[i] if U[i] < h else h
            na = a - x
            if na < L:
                na = L
            nb = b + x
            if nb > R:
                nb = R
            if na > nb:
                return False
            a, b = na, nb
        return True

    hi_bound = min(U[i] + D[i] for i in range(n))
    lo, hi = 0, hi_bound  # feasible(lo) is True; find max feasible
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    total = sum(U) + sum(D)
    print(total - n * lo)


main()
