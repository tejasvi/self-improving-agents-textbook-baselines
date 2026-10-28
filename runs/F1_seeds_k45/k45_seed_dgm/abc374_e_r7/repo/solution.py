def min_cost_for_capacity(processes, target_capacity):
    """
    Calculate the minimum cost to achieve at least target_capacity for each process.
    Returns the total cost, or float('inf') if impossible.
    """
    total_cost = 0
    
    for A, P, B, Q in processes:
        # For this process, we need to achieve target_capacity
        # We can use combinations of S machines and T machines
        # S: capacity A per unit, cost P per unit
        # T: capacity B per unit, cost Q per unit
        
        min_cost = float('inf')
        
        # Try all possible numbers of S machines
        # We need at most ceil(target_capacity / A) units of S machine alone
        max_s = (target_capacity + A - 1) // A  # This is ceil(target_capacity / A)
        
        for num_s in range(max_s + 1):
            capacity_from_s = num_s * A
            remaining_capacity = max(0, target_capacity - capacity_from_s)
            
            # How many T machines do we need?
            if remaining_capacity == 0:
                num_t = 0
            else:
                num_t = (remaining_capacity + B - 1) // B  # ceil division
            
            cost = num_s * P + num_t * Q
            min_cost = min(min_cost, cost)
        
        if min_cost == float('inf'):
            return float('inf')
        
        total_cost += min_cost
    
    return total_cost


def solve():
    N, X = map(int, input().split())
    processes = []
    for _ in range(N):
        A, P, B, Q = map(int, input().split())
        processes.append((A, P, B, Q))
    
    # Binary search on the answer
    # The maximum possible capacity is limited by the most efficient machine
    # In the worst case with budget X, we could buy X units of the cheapest machine
    max_possible = X * max(max(A, B) for A, P, B, Q in processes)
    
    left, right = 0, max_possible
    answer = 0
    
    while left <= right:
        mid = (left + right) // 2
        cost = min_cost_for_capacity(processes, mid)
        
        if cost <= X:
            answer = mid
            left = mid + 1
        else:
            right = mid - 1
    
    print(answer)


solve()
