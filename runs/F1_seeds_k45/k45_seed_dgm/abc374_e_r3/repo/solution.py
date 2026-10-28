import math

def min_cost_for_capacity(A, P, B, Q, target):
    """
    Find minimum cost to achieve at least 'target' products per day
    using combinations of machines with capacity A (cost P) and B (cost Q).
    """
    if target <= 0:
        return 0
    
    min_cost = float('inf')
    
    # Try different numbers of machine type 1 (S)
    # Maximum needed of type 1 is ceil(target / A)
    max_s = math.ceil(target / A)
    
    for num_s in range(max_s + 1):
        produced_by_s = num_s * A
        remaining = max(0, target - produced_by_s)
        
        # How many of type 2 (T) do we need?
        if remaining <= 0:
            num_t = 0
        else:
            num_t = math.ceil(remaining / B)
        
        cost = num_s * P + num_t * Q
        min_cost = min(min_cost, cost)
    
    return min_cost

def can_achieve_capacity(processes, X, target_capacity):
    """
    Check if we can achieve target_capacity with budget X.
    processes: list of (A, P, B, Q) tuples
    """
    total_cost = 0
    
    for A, P, B, Q in processes:
        cost = min_cost_for_capacity(A, P, B, Q, target_capacity)
        total_cost += cost
        if total_cost > X:
            return False
    
    return total_cost <= X

def solve():
    N, X = map(int, input().split())
    processes = []
    
    for _ in range(N):
        A, P, B, Q = map(int, input().split())
        processes.append((A, P, B, Q))
    
    # Binary search on the answer
    # Maximum possible capacity
    max_capacity = max(A for A, P, B, Q in processes) * X // min(P for A, P, B, Q in processes) + 1
    max_capacity = min(max_capacity, 10**10)  # Reasonable upper bound
    
    left, right = 0, max_capacity
    answer = 0
    
    while left <= right:
        mid = (left + right) // 2
        
        if can_achieve_capacity(processes, X, mid):
            answer = mid
            left = mid + 1
        else:
            right = mid - 1
    
    print(answer)

if __name__ == "__main__":
    solve()
