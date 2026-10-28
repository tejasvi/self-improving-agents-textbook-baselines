from collections import defaultdict

def solve():
    N, X = map(int, input().split())
    
    foods = []
    for _ in range(N):
        V, A, C = map(int, input().split())
        foods.append((V, A, C))
    
    # Separate foods by vitamin type
    vitamins = defaultdict(list)  # vitamin -> list of (amount, calories)
    for V, A, C in foods:
        vitamins[V].append((A, C))
    
    # Check if we have all three vitamins
    has_all_three = len(vitamins) == 3
    
    # For each vitamin type, compute minimum calories needed to get at least k units
    def min_calories_for_vitamin(vitamin_foods, target):
        """
        Returns minimum calories to get at least 'target' units of this vitamin.
        Returns infinity if impossible.
        """
        # DP: dp[c] = maximum units we can get with exactly c calories
        dp = [0] * (X + 1)
        
        for amount, calories in vitamin_foods:
            # Traverse backwards to avoid using same item twice
            for c in range(X, calories - 1, -1):
                dp[c] = max(dp[c], dp[c - calories] + amount)
        
        # Find minimum calories to get >= target
        for c in range(X + 1):
            if dp[c] >= target:
                return c
        
        return float('inf')
    
    def can_achieve(min_vitamin):
        """
        Check if we can achieve at least min_vitamin units of each vitamin
        within X calories total.
        """
        if not has_all_three:
            return min_vitamin == 0
        
        # For each vitamin, find minimum calories needed to get min_vitamin units
        min_cals = {}
        for v in [1, 2, 3]:
            min_cals[v] = min_calories_for_vitamin(vitamins[v], min_vitamin)
        
        # Check if we can achieve all three
        total = min_cals[1] + min_cals[2] + min_cals[3]
        return total <= X
    
    # Binary search on the answer
    left, right = 0, 200000
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
