def min_cost_for_capacity(A, P, B, Q, target_capacity):
    """
    Find the minimum cost to achieve at least target_capacity for a single process.
    
    We need: s*A + t*B >= target_capacity
    Cost: s*P + t*Q
    
    The cost function as a function of s is piecewise linear.
    We check critical values of s where the number of T machines needed changes.
    These occur at s where (target - s*A) crosses B boundaries.
    """
    if target_capacity <= 0:
        return 0
    
    min_cost = float('inf')
    
    # Strategy: check s values from 0 up to some reasonable limit
    # The cost changes as we increase s, and at some point using only S is cheaper
    # We only need to check enough values to find the minimum
    
    # Maximum s needed if we use only S machines
    max_s_only = (target_capacity + A - 1) // A
    
    # But we don't need to check all values. We can check:
    # 1. s = 0 (use only T)
    # 2. Small values of s (where we'd use T for remainder)
    # 3. s = max_s_only (use only S)
    
    # Since A, B <= 100, checking s from 0 to A*B or so should capture the minimum
    # Let's check s from 0 to min(max_s_only, A*B)
    
    max_s_to_check = min(max_s_only + 1, 150)  # Check up to a reasonable limit
    
    for s in range(max_s_to_check):
        capacity_from_s = s * A
        remaining = target_capacity - capacity_from_s
        
        if remaining <= 0:
            cost = s * P
        else:
            t = (remaining + B - 1) // B
            cost = s * P + t * Q
        
        min_cost = min(min_cost, cost)
    
    return min_cost


def can_achieve_capacity(machines, budget, target_capacity):
    """
    Check if we can achieve target_capacity for all processes within budget.
    """
    total_cost = 0
    
    for A, P, B, Q in machines:
        cost = min_cost_for_capacity(A, P, B, Q, target_capacity)
        total_cost += cost
        
        if total_cost > budget:
            return False
    
    return total_cost <= budget


def solve():
    N, X = map(int, input().split())
    
    machines = []
    for _ in range(N):
        A, P, B, Q = map(int, input().split())
        machines.append((A, P, B, Q))
    
    # Binary search on the production capacity
    # Upper bound: with unlimited budget, we could get very high capacity
    # But with budget X, the max is bounded. A reasonable estimate:
    left, right = 0, X * 100  # This should be safe as upper bound
    
    while left < right:
        mid = (left + right + 1) // 2
        
        if can_achieve_capacity(machines, X, mid):
            left = mid
        else:
            right = mid - 1
    
    print(left)


if __name__ == "__main__":
    solve()
