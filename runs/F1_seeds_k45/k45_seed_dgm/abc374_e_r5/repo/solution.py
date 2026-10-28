def min_cost_for_capacity(A, P, B, Q, target_capacity):
    """
    Find the minimum cost to achieve at least target_capacity.
    We can buy any number of machines S (capacity A, cost P) or T (capacity B, cost Q).
    
    This is essentially finding: min(count_s * P + count_t * Q)
    such that (count_s * A + count_t * B) >= target_capacity
    """
    if target_capacity <= 0:
        return 0
    
    min_cost = float('inf')
    
    # Try all possible counts of machine S (0 to max needed)
    # max needed is when we buy only S machines: ceil(target_capacity / A)
    max_s = (target_capacity + A - 1) // A  # This is ceil division
    
    for count_s in range(max_s + 1):
        capacity_from_s = count_s * A
        
        if capacity_from_s >= target_capacity:
            # We have enough capacity from S machines alone
            min_cost = min(min_cost, count_s * P)
        else:
            # We need some T machines
            remaining_capacity = target_capacity - capacity_from_s
            count_t = (remaining_capacity + B - 1) // B  # ceil division
            cost = count_s * P + count_t * Q
            min_cost = min(min_cost, cost)
    
    return min_cost


def can_achieve_capacity(processes, total_budget, target_capacity):
    """
    Check if we can achieve the target production capacity with the given budget.
    We need to achieve target_capacity for EACH process (all N processes must meet it).
    """
    total_cost = 0
    
    for A, P, B, Q in processes:
        cost = min_cost_for_capacity(A, P, B, Q, target_capacity)
        if cost == float('inf'):
            return False
        total_cost += cost
        if total_cost > total_budget:
            return False
    
    return total_cost <= total_budget


def solve():
    # Read input
    N, X = map(int, input().split())
    processes = []
    
    for _ in range(N):
        A, P, B, Q = map(int, input().split())
        processes.append((A, P, B, Q))
    
    # Binary search on the answer
    # The maximum possible capacity is limited by the most efficient machine
    # and the budget. An upper bound could be X * max(A, B) in theory, but we
    # can be more reasonable about it.
    
    # Find a reasonable upper bound
    max_capacity = X * 100  # Conservative upper bound
    
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
