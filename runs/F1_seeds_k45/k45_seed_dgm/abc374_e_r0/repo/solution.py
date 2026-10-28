# Write your solution here. Read from stdin, write to stdout.

def min_cost_for_capacity(A, P, B, Q, target):
    """
    Find minimum cost to achieve at least 'target' products for one process.
    Can buy x units of machine S (A products, P cost each)
    or y units of machine T (B products, Q cost each)
    Need: x*A + y*B >= target
    Minimize: x*P + y*Q
    """
    if target <= 0:
        return 0
    
    min_cost = float('inf')
    
    # Try all possible numbers of S machines
    # Maximum useful S machines is ceil(target / A)
    max_s = (target + A - 1) // A  # This is ceil(target / A)
    
    for s in range(max_s + 1):
        # With s units of S machine, we get s*A products
        remaining = target - s * A
        
        if remaining <= 0:
            # We already have enough from S machines
            cost = s * P
        else:
            # We need y units of T machine such that y*B >= remaining
            t = (remaining + B - 1) // B  # This is ceil(remaining / B)
            cost = s * P + t * Q
        
        min_cost = min(min_cost, cost)
    
    return min_cost


def can_achieve_capacity(processes, total_budget, target_capacity):
    """
    Check if we can achieve target_capacity for all processes within budget.
    processes: list of (A_i, P_i, B_i, Q_i)
    """
    total_cost = 0
    
    for A, P, B, Q in processes:
        cost = min_cost_for_capacity(A, P, B, Q, target_capacity)
        total_cost += cost
        
        if total_cost > total_budget:
            return False
    
    return total_cost <= total_budget


def solve(N, X, processes):
    """
    Binary search on the answer (production capacity).
    """
    # Binary search bounds
    left = 0
    right = 10**10  # Upper bound: max products per day
    
    answer = 0
    
    while left <= right:
        mid = (left + right) // 2
        
        if can_achieve_capacity(processes, X, mid):
            # We can achieve mid, try to do better
            answer = mid
            left = mid + 1
        else:
            # We cannot achieve mid, try less
            right = mid - 1
    
    return answer


# Read input
N, X = map(int, input().split())
processes = []

for _ in range(N):
    A, P, B, Q = map(int, input().split())
    processes.append((A, P, B, Q))

# Solve and print answer
result = solve(N, X, processes)
print(result)
