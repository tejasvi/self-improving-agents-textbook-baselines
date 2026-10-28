import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    x = int(data[1])
    U = []
    D = []
    idx = 2
    for _ in range(n):
        U.append(int(data[idx]))
        D.append(int(data[idx + 1]))
        idx += 2

    total = sum(U) + sum(D)
    hmax_bound = min(U[i] + D[i] for i in range(n))

    def feasible(h):
        # reachable interval for U'_i: [a, b]
        a = max(0, h - D[0])
        b = min(U[0], h)
        if a > b:
            return False
        for i in range(1, n):
            lo = h - D[i]
            if lo < 0:
                lo = 0
            hi = U[i] if U[i] < h else h
            na = a - x
            if lo < na:
                lo = na
            nb = b + x
            if hi > nb:
                hi = nb
            if lo > hi:
                return False
            a, b = lo, hi
        return True

    lo, hi = 0, hmax_bound  # lo always feasible
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1

    print(total - n * lo)


main()
