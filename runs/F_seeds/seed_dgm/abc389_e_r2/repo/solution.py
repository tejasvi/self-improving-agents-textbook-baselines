import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    M = int(data[1])
    P = [int(x) for x in data[2:2 + n]]

    def stats(T):
        # count and total cost of all marginal unit costs (2j-1)*p <= T, capped early
        c = 0
        S = 0
        for p in P:
            m = ((T // p) + 1) // 2
            if m:
                c += m
                S += p * m * m
                if S > M:
                    return c, S
        return c, S

    # S(T) is nondecreasing in T; find largest T with S(T) <= M.
    lo, hi = 0, 10 ** 15  # S(hi) > M for all inputs within constraints
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if stats(mid)[1] <= M:
            lo = mid
        else:
            hi = mid - 1
    T = lo
    c, S = stats(T)
    ans = c + (M - S) // (T + 1)
    print(ans)


main()
