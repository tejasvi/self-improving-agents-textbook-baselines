# Write your solution here. Read from stdin, write to stdout.

def solve():
    N, X = map(int, input().split())
    
    # Separate foods by vitamin type
    foods = [[] for _ in range(4)]  # foods[1], foods[2], foods[3]
    
    for _ in range(N):
        V, A, C = map(int, input().split())
        foods[V].append((A, C))
    
    # For each vitamin type, compute the minimum calories needed to get at least k units
    # dp[v][k] = minimum calories to get at least k units of vitamin v
    def compute_min_calories(food_list, max_amount):
        """
        For a given food list, compute minimum calories needed to get at least k units
        Returns a list where result[k] = minimum calories to get at least k units
        """
        # Use DP: dp[amount] = minimum calories to get at least amount
        # We'll use a different approach: knapsack-like DP
        # dp[cal] = maximum amount of vitamin we can get with exactly cal calories
        
        dp = [0] * (X + 1)
        
        for amount, cost in food_list:
            # Process in reverse to avoid using same item multiple times
            for cal in range(X, cost - 1, -1):
                dp[cal] = max(dp[cal], dp[cal - cost] + amount)
        
        return dp
    
    # For each vitamin, get DP table showing max amount achievable with given calories
    dp_vitamins = [None] * 4
    for v in range(1, 4):
        dp_vitamins[v] = compute_min_calories(foods[v], X)
    
    # Binary search on the answer
    def can_achieve(min_val):
        """Check if we can get at least min_val of each vitamin within X calories"""
        # Try all possible allocations of calories to the three vitamins
        # We need: amount1 >= min_val, amount2 >= min_val, amount3 >= min_val
        # And: cal1 + cal2 + cal3 <= X
        
        for cal1 in range(X + 1):
            for cal2 in range(X + 1 - cal1):
                cal3 = X - cal1 - cal2
                
                # Check if we can get min_val of each vitamin with these calories
                if (dp_vitamins[1][cal1] >= min_val and
                    dp_vitamins[2][cal2] >= min_val and
                    dp_vitamins[3][cal3] >= min_val):
                    return True
        
        return False
    
    # Binary search for the answer
    left, right = 0, max(a for v in range(1, 4) for a, c in foods[v]) if any(foods[v] for v in range(1, 4)) else 0
    
    answer = 0
    while left <= right:
        mid = (left + right) // 2
        if can_achieve(mid):
            answer = mid
            left = mid + 1
        else:
            right = mid - 1
    
    print(answer)

solve()
