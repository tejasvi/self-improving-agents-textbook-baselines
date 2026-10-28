import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    m = int(data[1])
    P = [int(x) for x in data[2:2 + n]]

    def stats(T):
        # count and total cost of all marginal units with cost <= T
        c = 0
        s = 0
        for p in P:
            k = ((T // p) + 1) >> 1
            if k:
                c += k
                s += k * k * p
        return c, s

    # largest T with s(T) <= m; s(0) = 0 <= m
    lo, hi = 0, 4 * 10 ** 14  # s(hi) > m guaranteed for these bounds
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if stats(mid)[1] <= m:
            lo = mid
        else:
            hi = mid - 1
    T = lo
    c, s = stats(T)
    print(c + (m - s) // (T + 1))


main()
