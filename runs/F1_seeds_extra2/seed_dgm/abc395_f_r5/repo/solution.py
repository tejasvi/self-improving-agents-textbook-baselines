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
        # Choose final upper lengths u_i in [max(0, h-D_i), min(U_i, h)]
        # with |u_i - u_{i+1}| <= x. Track reachable interval [lo, hi].
        lo = max(0, h - D[0])
        hi = min(U[0], h)
        if lo > hi:
            return False
        for i in range(1, n):
            a = h - D[i]
            if a < 0:
                a = 0
            b = U[i] if U[i] < h else h
            t = lo - x
            if t > a:
                a = t
            t = hi + x
            if t < b:
                b = t
            if a > b:
                return False
            lo = a
            hi = b
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
