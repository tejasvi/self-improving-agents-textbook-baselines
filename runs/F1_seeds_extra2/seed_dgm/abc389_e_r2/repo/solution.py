import sys
from math import isqrt


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    m = int(data[1])
    p = [int(x) for x in data[2:2 + n]]

    def stats(t):
        # For threshold t: units of product i with marginal cost <= t
        # are j with P*(2j-1) <= t, i.e. c = (t//P + 1)//2 units,
        # costing P*c^2 in total.
        cnt = 0
        cost = 0
        for q in p:
            c = (t // q + 1) >> 1
            if c:
                cnt += c
                cost += q * c * c
        return cnt, cost

    pmin = min(p)
    # cost(hi) > m guaranteed for hi below
    lo = 0
    hi = 2 * isqrt(m * pmin) + 4 * pmin + 10
    while stats(hi)[1] <= m:
        hi *= 2
    # invariant: cost(lo) <= m, cost(hi) > m
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if stats(mid)[1] <= m:
            lo = mid
        else:
            hi = mid
    cnt, cost = stats(lo)
    ans = cnt + (m - cost) // (lo + 1)
    print(ans)


main()
