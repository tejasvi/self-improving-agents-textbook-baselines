import sys
from math import isqrt


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    m = int(data[1])
    P = [int(x) for x in data[2:2 + n]]
    pmin = min(P)

    # Buying the j-th unit of product i costs P_i*(2j-1) (marginal).
    # Units with marginal <= X for product i: c_i = (X//P_i + 1)//2,
    # with total cost P_i * c_i^2.
    def stats(X):
        cnt = 0
        cost = 0
        for p in P:
            c = (X // p + 1) >> 1
            if c:
                cost += p * c * c
                if cost > m:
                    return None
                cnt += c
        return cnt, cost

    # hi is guaranteed infeasible: product with pmin alone exceeds m.
    hi = 2 * pmin * (isqrt(m // pmin) + 2) + 2 * pmin
    lo = 0  # cost(0) = 0 is feasible
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if stats(mid) is not None:
            lo = mid
        else:
            hi = mid
    X = lo
    cnt, cost = stats(X)
    # Next marginal price is X+1; cost(X+1) > m implies the extra count
    # floor((m-cost)/(X+1)) is less than the number of units priced X+1.
    extra = (m - cost) // (X + 1)
    print(cnt + extra)


main()
