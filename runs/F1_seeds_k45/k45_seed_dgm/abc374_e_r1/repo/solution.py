# Write your solution here. Read from stdin, write to stdout.

def min_cost_for_capacity(processes, target_capacity):
    """
    For a given target capacity, calculate the minimum cost to achieve it.
    For each process, we need to find the minimum cost to get at least target_capacity.
    
    Returns the minimum total cost, or float('inf') if impossible.
    """
    total_cost = 0
    
    for a, p, b, q in processes:
        # For this process, find minimum cost to achieve target_capacity
        # We can combine S and T machines
        
        min_cost_for_this_process = float('inf')
        
        # Try all possible combinations of S and T machines
        # For S machines: we need at least ceil(target_capacity / a) units
        # For T machines: we need at least ceil(target_capacity / b) units
        
        max_s_needed = (target_capacity + a - 1) // a  # ceiling division
        max_t_needed = (target_capacity + b - 1) // b
        
        # Try buying only S machines
        cost_only_s = max_s_needed * p
        if max_s_needed * a >= target_capacity:
            min_cost_for_this_process = min(min_cost_for_this_process, cost_only_s)
        
        # Try buying only T machines
        cost_only_t = max_t_needed * q
        if max_t_needed * b >= target_capacity:
            min_cost_for_this_process = min(min_cost_for_this_process, cost_only_t)
        
        # Try combinations of S and T machines
        # For each number of S machines from 0 to max_s_needed
        for num_s in range(max_s_needed + 1):
            capacity_from_s = num_s * a
            remaining_capacity = max(0, target_capacity - capacity_from_s)
            
            if remaining_capacity == 0:
                # We achieved the target with only S machines
                cost = num_s * p
                min_cost_for_this_process = min(min_cost_for_this_process, cost)
            else:
                # We need some T machines
                num_t_needed = (remaining_capacity + b - 1) // b
                cost = num_s * p + num_t_needed * q
                min_cost_for_this_process = min(min_cost_for_this_process, cost)
        
        if min_cost_for_this_process == float('inf'):
            return float('inf')
        
        total_cost += min_cost_for_this_process
    
    return total_cost


def solve():
    n, x = map(int, input().split())
    processes = []
    for _ in range(n):
        a, p, b, q = map(int, input().split())
        processes.append((a, p, b, q))
    
    # Binary search on the answer
    # The minimum possible answer is 0
    # The maximum possible answer is bounded by the maximum capacity we could get
    
    # Find upper bound: if we spend all budget on the machine with best efficiency
    max_efficiency = 0
    for a, p, b, q in processes:
        max_efficiency = max(max_efficiency, a / p, b / q)
    
    # Upper bound on production capacity
    upper_bound = int(x * max_efficiency) + 1
    
    left, right = 0, upper_bound
    answer = 0
    
    while left <= right:
        mid = (left + right) // 2
        cost = min_cost_for_capacity(processes, mid)
        
        if cost <= x:
            answer = mid
            left = mid + 1
        else:
            right = mid - 1
    
    print(answer)


if __name__ == "__main__":
    solve()
