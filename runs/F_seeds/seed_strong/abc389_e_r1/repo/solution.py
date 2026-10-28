import sys
from operator import mul


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    M = int(data[1])
    P = list(map(int, data[2:2 + n]))

    # Buying k units of product i costs k^2 * P_i; the j-th unit costs (2j-1)*P_i.
    # Greedily take the cheapest marginal units. For threshold t, the number of
    # units with marginal cost <= t is cnt(t) = sum floor((floor(t/P)+1)/2) and
    # their total cost is cost(t) = sum c_i^2 * P_i.
    def stats(t):
        q = [((t // p) + 1) >> 1 for p in P]
        cnt = sum(q)
        cost = sum(map(mul, map(mul, q, q), P))
        return cnt, cost

    # Largest t with cost(t) <= M. cost(0) = 0 <= M.
    # Upper bound: a single product with P=1 gives marginal costs up to ~2*sqrt(M)*...;
    # t = 2*sqrt(M*P_min)+ something; use a safe bound where cost exceeds M.
    from math import isqrt
    pmin = min(P)
    lo = 0
    hi = 2 * isqrt(M * pmin) + 4 * pmin + 4
    while stats(hi)[1] <= M:
        lo = hi
        hi *= 2
    # invariant: cost(lo) <= M < cost(hi)
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if stats(mid)[1] <= M:
            lo = mid
        else:
            hi = mid
    t = lo
    cnt, cost = stats(t)
    cnt_next, _ = stats(t + 1)
    R = M - cost
    extra = min(R // (t + 1), cnt_next - cnt)
    print(cnt + extra)


main()
