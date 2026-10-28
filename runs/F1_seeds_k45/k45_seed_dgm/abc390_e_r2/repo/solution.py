# Write your solution here. Read from stdin, write to stdout.

def can_achieve(foods, X, min_vitamins):
    """
    Check if we can achieve at least min_vitamins of each vitamin type
    within X calories using the given foods.
    """
    # Group foods by vitamin type
    foods_by_vitamin = [[], [], []]
    for v, a, c in foods:
        foods_by_vitamin[v - 1].append((a, c))
    
    # For each vitamin type, find minimum cost to get at least min_vitamins
    min_costs = []
    
    for vitamin_idx in range(3):
        # Find minimum cost to get at least min_vitamins of this vitamin
        items = foods_by_vitamin[vitamin_idx]
        
        # DP for knapsack: dp[j] = max vitamin amount with exactly j calories
        dp = [0] * (X + 1)
        
        for a, c in items:
            # Traverse backwards to avoid using same item multiple times
            for j in range(X, c - 1, -1):
                dp[j] = max(dp[j], dp[j - c] + a)
        
        # Find minimum cost to get at least min_vitamins
        min_cost = float('inf')
        for j in range(X + 1):
            if dp[j] >= min_vitamins:
                min_cost = min(min_cost, j)
        
        min_costs.append(min_cost)
    
    # Check if total cost is within X
    return sum(min_costs) <= X


def solve():
    # Read input
    N, X = map(int, input().split())
    foods = []
    for _ in range(N):
        V, A, C = map(int, input().split())
        foods.append((V, A, C))
    
    # Binary search on the answer
    left, right = 0, 2 * 10**5
    answer = 0
    
    while left <= right:
        mid = (left + right) // 2
        if can_achieve(foods, X, mid):
            answer = mid
            left = mid + 1
        else:
            right = mid - 1
    
    print(answer)

solve()
