# Write your solution here. Read from stdin, write to stdout.

import sys
import math

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    P = [int(next(it)) for _ in range(N)]

    # binary search on marginal cost lambda
    # function to compute total cost for given lambda (include all units with marginal <= lambda)
    def total_cost_and_units(lam):
        total_units = 0
        total_cost = 0
        for p in P:
            # max k such that (2k-1)*p <= lam
            k = (lam // p + 1) // 2
            if k:
                total_units += k
                total_cost += p * k * k
        return total_units, total_cost

    # upper bound for lambda
    max_p = max(P)
    min_p = min(P)
    # maximum possible k per product is sqrt(M / min_p) (rough estimate)
    max_k_est = int(math.isqrt(M // min_p)) + 2
    high = max_p * (2 * max_k_est + 1)  # safe upper bound
    low = 0
    while low < high:
        mid = (low + high + 1) // 2
        _, cost = total_cost_and_units(mid)
        if cost <= M:
            low = mid
        else:
            high = mid - 1
    lam = low
    units, cost_sofar = total_cost_and_units(lam)
    remaining = M - cost_sofar
    # gather next marginal costs
    next_costs = []
    for p in P:
        k = (lam // p + 1) // 2
        # next marginal cost after buying k units
        next_c = (2 * k + 1) * p
        next_costs.append(next_c)
    next_costs.sort()
    for c in next_costs:
        if c <= remaining:
            remaining -= c
            units += 1
        else:
            break
    print(units)

if __name__ == "__main__":
    solve()
