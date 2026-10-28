# Solution for Sensor Optimization Dilemma 2
# We binary search the answer (maximum production capacity) and for each candidate value k
# compute the minimal cost needed for each process to achieve at least k products per day.
# For a single process we have two machine types with capacities A, B and costs P, Q.
# The minimal cost to reach at least k can be found by enumerating a bounded number of one machine type
# (at most the capacity of the other type) and filling the rest with the other type.
# Since A,B <= 100 this enumeration is O(100) per process, which is fast enough.

import sys

def min_cost_for_process(k, A, P, B, Q):
    """Return minimal cost to achieve at least k capacity using machines (A,P) and (B,Q).
    A, B are positive integers (capacity per unit), P, Q are costs per unit.
    """
    # If k == 0, cost is 0
    if k <= 0:
        return 0
    # Simple shortcuts: only one type
    cost_only_A = ((k + A - 1) // A) * P
    cost_only_B = ((k + B - 1) // B) * Q
    best = min(cost_only_A, cost_only_B)
    # Enumerate number of A machines from 0 up to min(B-1, ceil(k/A))
    limit_a = min(B - 1, (k + A - 1) // A)
    for x in range(limit_a + 1):
        remaining = k - x * A
        if remaining <= 0:
            cost = x * P
        else:
            y = (remaining + B - 1) // B
            cost = x * P + y * Q
        if cost < best:
            best = cost
    # Enumerate number of B machines analogously
    limit_b = min(A - 1, (k + B - 1) // B)
    for y in range(limit_b + 1):
        remaining = k - y * B
        if remaining <= 0:
            cost = y * Q
        else:
            x = (remaining + A - 1) // A
            cost = x * P + y * Q
        if cost < best:
            best = cost
    return best


def feasible(k, processes, budget):
    total = 0
    for A, P, B, Q in processes:
        total += min_cost_for_process(k, A, P, B, Q)
        if total > budget:
            return False
    return total <= budget


def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    X = int(next(it))
    processes = []
    for _ in range(N):
        A = int(next(it))
        P = int(next(it))
        B = int(next(it))
        Q = int(next(it))
        processes.append((A, P, B, Q))
    # Upper bound for binary search: even if we spend all budget on the most cost‑effective machine
    # across all processes, the capacity per process cannot exceed (max capacity per unit) * (budget / min cost per unit).
    max_cap_per_unit = max(max(A, B) for A, _, B, _ in processes)
    min_cost_per_unit = min(min(P / A, Q / B) for A, P, B, Q in processes)
    # Use a safe integer upper bound
    high = int(max_cap_per_unit * X // min_cost_per_unit) + 1
    # Ensure high is at least 1 for the binary search loop
    if high < 1:
        high = 1
    low = 0
    while low + 1 < high:
        mid = (low + high) // 2
        if feasible(mid, processes, X):
            low = mid
        else:
            high = mid
    print(low)

if __name__ == "__main__":
    solve()
