# Write your solution here. Read from stdin, write to stdout.

import sys
import math


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    P = [int(next(it)) for _ in range(N)]

    # Upper bound for total units: each product i can contribute at most sqrt(M / P_i)
    ub = 0
    for p in P:
        ub += int(math.isqrt(M // p))

    # Helper: for a given marginal cost threshold C, return total units obtainable and total cost
    def total_units_and_cost(C: int):
        units = 0
        cost = 0
        for p in P:
            if C < p:
                continue
            # maximum k such that (2k-1)*p <= C
            k = (C // p + 1) // 2
            units += k
            cost += p * k * k
        return units, cost

    # Check if we can achieve at least X units within budget M
    def feasible(X: int) -> bool:
        if X <= 0:
            return True
        # Binary search the minimal marginal cost C so that we can get >= X units
        low, high = 0, 2 * 10**18  # sufficiently large upper bound
        while low < high:
            mid = (low + high) // 2
            units, _ = total_units_and_cost(mid)
            if units >= X:
                high = mid
            else:
                low = mid + 1
        C = low  # minimal marginal cost achieving at least X units
        # Compute units and cost using strictly cheaper marginal costs (C-1)
        units_less, cost_less = total_units_and_cost(C - 1)
        need = X - units_less  # number of units we must take with marginal cost exactly C
        total_cost = cost_less + need * C
        return total_cost <= M

    # Binary search the answer
    lo, hi = 0, ub
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    print(lo)


if __name__ == "__main__":
    solve()
