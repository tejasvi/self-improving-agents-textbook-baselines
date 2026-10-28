import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    m = int(data[1])
    P = [int(x) for x in data[2:2 + n]]

    def stats(T):
        # Number of units and total cost when taking all marginal costs <= T.
        # Marginal cost of the k-th unit of product i is (2k-1)*P_i.
        cnt = 0
        cost = 0
        for p in P:
            k = (T // p + 1) // 2
            if k:
                cnt += k
                cost += p * k * k
        return cnt, cost

    lo = 0                  # feasible: nothing bought, cost 0 <= m
    hi = 4 * 10 ** 14       # infeasible for all inputs within constraints
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if stats(mid)[1] <= m:
            lo = mid
        else:
            hi = mid
    cnt, cost = stats(lo)
    # All marginal costs <= lo are taken. Since lo+1 is infeasible, the units
    # priced exactly lo+1 number c with c*(lo+1) > m-cost, so we can afford
    # floor((m-cost)/(lo+1)) of them, which is optimal.
    ans = cnt + (m - cost) // (lo + 1)
    print(ans)


main()
