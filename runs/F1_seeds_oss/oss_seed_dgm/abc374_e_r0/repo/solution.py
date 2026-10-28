# Write your solution here. Read from stdin, write to stdout.
import sys

def min_cost_for_capacity(A, P, B, Q, C):
    """Return minimal cost to achieve at least C capacity using machines S (A,P) and T (B,Q).
    A, B <= 100, costs up to 1e7, C can be large.
    The optimal solution can be found by trying small counts of one type up to the other's capacity.
    """
    if C <= 0:
        return 0
    INF = 10**30
    # pure S or pure T
    a_needed = (C + A - 1) // A
    ans = a_needed * P
    b_needed = (C + B - 1) // B
    ans = min(ans, b_needed * Q)
    # mix: iterate a from 0 to B-1 (inclusive) and compute needed b
    for a in range(min(B, a_needed + 1)):
        remaining = C - a * A
        if remaining <= 0:
            cost = a * P
        else:
            b = (remaining + B - 1) // B
            cost = a * P + b * Q
        if cost < ans:
            ans = cost
    # iterate b from 0 to A-1 (inclusive)
    for b in range(min(A, b_needed + 1)):
        remaining = C - b * B
        if remaining <= 0:
            cost = b * Q
        else:
            a = (remaining + A - 1) // A
            cost = b * Q + a * P
        if cost < ans:
            ans = cost
    return ans

def feasible(target, processes, budget):
    total = 0
    for A, P, B, Q in processes:
        cost = min_cost_for_capacity(A, P, B, Q, target)
        total += cost
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
        A = int(next(it)); P = int(next(it)); B = int(next(it)); Q = int(next(it))
        processes.append((A, P, B, Q))
    # Compute an upper bound for binary search: for each process, the max capacity reachable if we spend all budget on the cheaper per-unit machine.
    upper = None
    for A, P, B, Q in processes:
        cap_s = A * (X // P)  # spend all on S machines
        cap_t = B * (X // Q)  # spend all on T machines
        max_cap = max(cap_s, cap_t)
        if upper is None or max_cap < upper:
            upper = max_cap
    if upper is None:
        upper = 0
    low, high = 0, upper
    while low < high:
        mid = (low + high + 1) // 2
        if feasible(mid, processes, X):
            low = mid
        else:
            high = mid - 1
    print(low)

if __name__ == "__main__":
    solve()
