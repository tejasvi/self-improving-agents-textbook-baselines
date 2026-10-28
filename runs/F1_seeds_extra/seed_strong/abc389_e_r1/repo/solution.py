import sys
from math import isqrt
from operator import mul

def main():
    data = sys.stdin.read().split()
    n = int(data[0]); M = int(data[1])
    P = [int(x) for x in data[2:2 + n]]
    pmin = min(P)
    # Any feasible threshold X satisfies X <= 2*sqrt(M*pmin) + pmin, so this hi is infeasible.
    lo = 0
    hi = 2 * isqrt(M * pmin) + 2 * pmin + 2

    def cost(X):
        cs = [((X // p) + 1) >> 1 for p in P]
        return sum(map(mul, P, map(mul, cs, cs))), cs

    while hi - lo > 1:
        mid = (lo + hi) // 2
        if cost(mid)[0] <= M:
            lo = mid
        else:
            hi = mid
    S, cs = cost(lo)
    cnt = sum(cs)
    r = (M - S) // (lo + 1)
    print(cnt + r)

main()
