import math

def min_cost_for_target(target, A, P, B, Q):
    """
    Find minimum cost to achieve at least 'target' capacity.
    Can use x units of machine S (capacity A, cost P) and y units of machine T (capacity B, cost Q).
    """
    if target <= 0:
        return 0
    
    min_cost = float('inf')
    
    # Try using only S machines
    s_only = math.ceil(target / A)
    min_cost = min(min_cost, s_only * P)
    
    # Try using only T machines
    t_only = math.ceil(target / B)
    min_cost = min(min_cost, t_only * Q)
    
    # Try combinations: iterate through number of S machines
    # For efficiency, we only need to check a reasonable range
    # The maximum number of S to consider is the cost where it equals using T only
    for num_s in range(0, t_only + 1):
        capacity_from_s = num_s * A
        remaining_capacity = max(0, target - capacity_from_s)
        num_t = math.ceil(remaining_capacity / B) if remaining_capacity > 0 else 0
        cost = num_s * P + num_t * Q
        min_cost = min(min_cost, cost)
    
    # Similarly, iterate through number of T machines
    for num_t in range(0, s_only + 1):
        capacity_from_t = num_t * B
        remaining_capacity = max(0, target - capacity_from_t)
        num_s = math.ceil(remaining_capacity / A) if remaining_capacity > 0 else 0
        cost = num_s * P + num_t * Q
        min_cost = min(min_cost, cost)
    
    return min_cost


def can_achieve(target, processes, budget):
    """
    Check if we can achieve the target production capacity with the given budget.
    For each process, find the minimum cost to achieve target capacity.
    """
    total_cost = 0
    
    for A, P, B, Q in processes:
        min_cost = min_cost_for_target(target, A, P, B, Q)
        total_cost += min_cost
        
        if total_cost > budget:
            return False
    
    return total_cost <= budget


def solve():
    N, X = map(int, input().split())
    processes = []
    
    for _ in range(N):
        A, P, B, Q = map(int, input().split())
        processes.append((A, P, B, Q))
    
    # Binary search on the answer
    left = 0
    right = 10**10  # Safe upper bound
    
    answer = 0
    
    while left <= right:
        mid = (left + right) // 2
        
        if can_achieve(mid, processes, X):
            answer = mid
            left = mid + 1
        else:
            right = mid - 1
    
    print(answer)

solve()
