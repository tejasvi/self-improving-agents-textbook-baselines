import sys
from math import isqrt


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    m = int(data[1])
    P = [int(x) for x in data[2:2 + n]]
    pmin = min(P)

    def cost(X):
        return sum(p * (((X // p) + 1) >> 1) ** 2 for p in P)

    def count(X):
        return sum(((X // p) + 1) >> 1 for p in P)

    # Upper bound: with only the cheapest product, units ~ X/(2p), cost ~ p*(X/2p)^2
    # so X ~ 2*sqrt(m*p). Use a safe starting bound and grow if needed.
    hi = 2 * isqrt(m // pmin) + 4
    while cost(hi) <= m:
        hi *= 2
    lo = 0
    # invariant: cost(lo) <= m < cost(hi)
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if cost(mid) <= m:
            lo = mid
        else:
            hi = mid
    rem = m - cost(lo)
    cnt = count(lo)
    cnt1 = count(lo + 1)
    extra = min(cnt1 - cnt, rem // (lo + 1))
    print(cnt + extra)


main()
