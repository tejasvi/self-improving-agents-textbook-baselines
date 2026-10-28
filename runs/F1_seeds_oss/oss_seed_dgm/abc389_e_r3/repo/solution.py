# Write your solution here. Read from stdin, write to stdout.
import sys

def compute_units_cost_limited(P, C, limit):
    """Return (total_units, total_cost). If total_cost exceeds *limit*, stop early and return (units, cost) where cost > limit.
    This avoids huge integer calculations during binary search.
    """
    total_units = 0
    total_cost = 0
    for p in P:
        k = (C // p + 1) // 2
        if k:
            total_units += k
            # contribution may exceed limit, check before adding fully
            # if k is large, p*k*k could be huge; we can compare using division
            # but Python int handles it, we just break when cost > limit to limit work.
            total_cost += p * k * k
            if total_cost > limit:
                # early exit
                return total_units, total_cost
    return total_units, total_cost

def compute_units_and_cost(P, C):
    """Exact computation of total units and cost (used after binary search when cost <= M)."""
    total_units = 0
    total_cost = 0
    for p in P:
        k = (C // p + 1) // 2
        if k:
            total_units += k
            total_cost += p * k * k
    return total_units, total_cost


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    P = [int(next(it)) for _ in range(N)]

    # Binary search for the largest marginal cost C such that total_cost(C) <= M.
    lo = 0  # total_cost(lo) <= M
    hi = 2 * M + 1  # safe upper bound; total_cost(hi) will exceed M
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        _, cost = compute_units_cost_limited(P, mid, M)
        if cost <= M:
            lo = mid
        else:
            hi = mid
    C = lo

    # Units and cost with all marginal costs <= C (this cost is guaranteed <= M).
    units, cost = compute_units_and_cost(P, C)
    remaining = M - cost

    # Prepare list of next marginal costs for buying one more unit from each product.
    next_costs = []
    for p in P:
        k = (C // p + 1) // 2
        next_costs.append((2 * k + 1) * p)
    next_costs.sort()

    for nc in next_costs:
        if remaining >= nc:
            remaining -= nc
            units += 1
        else:
            break

    print(units)

if __name__ == "__main__":
    solve()
