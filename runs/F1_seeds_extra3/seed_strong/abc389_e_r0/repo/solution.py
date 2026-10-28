import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); m = int(data[1])
    P = [int(x) for x in data[2:2 + n]]

    def counts(T):
        return [(T // p + 1) >> 1 for p in P]

    def cost(T):
        return sum(c * c * p for c, p in zip(counts(T), P))

    # max T with cost(T) <= m; cost(0) = 0 <= m. hi is infeasible for m <= 1e18.
    lo, hi = 0, 4 * 10**9  # cost(4e9) >= 4e18 > m
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if cost(mid) <= m:
            lo = mid
        else:
            hi = mid - 1
    T = lo
    c = counts(T)
    S = sum(x * x * p for x, p in zip(c, P))
    C = sum(c)
    ans = C + (m - S) // (T + 1)
    print(ans)

main()
