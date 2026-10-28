import sys
from operator import floordiv, mul


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    M = int(data[1])
    P = [int(x) for x in data[2:2 + n]]

    def stats(X):
        # c_i = number of marginal units of product i with cost <= X
        cs = [(x + 1) >> 1 for x in map(X.__floordiv__, P)]
        C = sum(cs)
        S = sum(map(mul, map(mul, cs, cs), P))
        return C, S

    # largest X with S(X) <= M; S(0)=0 feasible, S(hi) > M for hi large
    lo, hi = 0, 3 * 10 ** 14
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if stats(mid)[1] <= M:
            lo = mid
        else:
            hi = mid
    X = lo
    C, S = stats(X)
    ans = C + (M - S) // (X + 1)
    print(ans)


main()
