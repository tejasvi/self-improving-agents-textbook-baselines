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

    # Helper: compute total units and cost for a given marginal cost threshold lam
    def compute(lam):
        total_units = 0
        total_cost = 0
        # also compute next marginal costs for each product
        next_costs = []
        for pi in P:
            # maximum t such that pi * (2t-1) <= lam
            # t = floor((lam / pi + 1) // 2)
            if lam < pi:  # cannot buy even one unit
                t = 0
            else:
                t = (lam // pi + 1) // 2
            total_units += t
            total_cost += pi * t * t
            # next marginal cost if we buy one more unit
            next_marg = pi * (2 * t + 1)
            next_costs.append(next_marg)
        return total_units, total_cost, next_costs

    # Upper bound for lambda (maximum marginal cost we might consider)
    max_pi = max(P)
    # maximum possible units per product is sqrt(M / min_pi), use that for safe bound
    min_pi = min(P)
    max_k = int(math.isqrt(M // min_pi)) + 2
    high_lambda = max_pi * (2 * max_k + 1)  # safe upper bound
    low = 0
    high = high_lambda
    while low < high:
        mid = (low + high + 1) // 2
        _, cost, _ = compute(mid)
        if cost <= M:
            low = mid
        else:
            high = mid - 1
    lam = low
    units, cost, next_costs = compute(lam)
    remaining = M - cost
    # take additional units greedily from next_costs (sorted)
    next_costs.sort()
    for c in next_costs:
        if remaining >= c:
            remaining -= c
            units += 1
        else:
            break
    print(units)

if __name__ == "__main__":
    solve()
