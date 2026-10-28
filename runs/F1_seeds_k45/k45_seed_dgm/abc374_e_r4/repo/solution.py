import sys
from typing import List, Tuple

def min_cost_for_capacity(capacity: int, machine_specs: List[Tuple[int, int, int, int]]) -> int:
    """
    Calculate the minimum cost to achieve at least 'capacity' for all processes.
    
    Args:
        capacity: Target capacity for each process
        machine_specs: List of (A_i, P_i, B_i, Q_i) for each process
    
    Returns:
        Minimum cost to achieve this capacity for all processes
    """
    total_cost = 0
    
    for A, P, B, Q in machine_specs:
        # For this process, find minimum cost to achieve 'capacity'
        # We can buy x units of S (capacity A, cost P each) and y units of T (capacity B, cost Q each)
        # We need: x*A + y*B >= capacity
        # We want to minimize: x*P + y*Q
        
        min_process_cost = float('inf')
        
        # Maximum units of A needed (if we use only A)
        max_x = (capacity + A - 1) // A
        
        # We need to check the critical points where the cost function might change
        # The cost changes based on x mod B (effectively)
        # We check from max(0, max_x - 101) to max_x since max(B) <= 100
        
        # This ensures we check enough values to find the true minimum
        for x in range(max(0, max_x - 101), max_x + 1):
            remaining_capacity = capacity - x * A
            
            if remaining_capacity <= 0:
                cost = x * P
            else:
                y = (remaining_capacity + B - 1) // B
                cost = x * P + y * Q
            
            min_process_cost = min(min_process_cost, cost)
        
        total_cost += min_process_cost
    
    return total_cost


def can_achieve_capacity(capacity: int, machine_specs: List[Tuple[int, int, int, int]], budget: int) -> bool:
    """Check if the given capacity can be achieved within budget."""
    cost = min_cost_for_capacity(capacity, machine_specs)
    return cost <= budget


def solve():
    # Read input
    N, X = map(int, input().split())
    machine_specs = []
    
    for _ in range(N):
        A, P, B, Q = map(int, input().split())
        machine_specs.append((A, P, B, Q))
    
    # Binary search on the answer
    left = 0
    right = X * 100  # Since max(A_i, B_i) <= 100
    
    while left < right:
        mid = (left + right + 1) // 2  # Use upper middle to avoid infinite loop
        
        if can_achieve_capacity(mid, machine_specs, X):
            left = mid
        else:
            right = mid - 1
    
    print(left)


if __name__ == "__main__":
    solve()
