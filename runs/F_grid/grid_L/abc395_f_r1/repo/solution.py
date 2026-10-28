import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    x = int(data[1])
    U = [0] * n
    D = [0] * n
    total = 0
    for i in range(n):
        u = int(data[2 + 2 * i])
        d = int(data[3 + 2 * i])
        U[i] = u
        D[i] = d
        total += u + d

    # Feasibility is monotone in H (if H is feasible, so is H-1),
    # so binary search for the largest feasible H.
    def feasible(h):
        # reachable set of values for U'_i is an interval [a, b]
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

    lo = 0
    hi = min(U[i] + D[i] for i in range(n))
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1

    print(total - n * lo)


main()
