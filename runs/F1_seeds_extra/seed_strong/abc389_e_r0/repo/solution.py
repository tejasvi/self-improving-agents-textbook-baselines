import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    M = int(data[1])
    P = [int(x) for x in data[2:2 + n]]

    def stats(T):
        # returns (count, cost) of all units with marginal cost (2k-1)*P_i <= T
        cnt = 0
        cost = 0
        for p in P:
            c = ((T // p) + 1) // 2
            if c:
                cnt += c
                cost += p * c * c
        return cnt, cost

    # Estimate threshold: cost(T) ~ T^2 * W / 4, W = sum(1/P_i)
    W = sum(1.0 / p for p in P)
    T0 = int(2.0 * (M / W) ** 0.5)
    Pmax = max(P)
    D = 4 * Pmax + 10

    def fits(T):
        return stats(T)[1] <= M

    # bracket: lo fits, hi does not
    lo = max(0, T0 - D)
    while lo > 0 and not fits(lo):
        lo = max(0, lo - 2 * D)
        D *= 2
    hi = T0 + D
    while fits(hi):
        hi = hi + 2 * D
        D *= 2
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if fits(mid):
            lo = mid
        else:
            hi = mid
    cnt, cost = stats(lo)
    print(cnt + (M - cost) // (lo + 1))


main()
