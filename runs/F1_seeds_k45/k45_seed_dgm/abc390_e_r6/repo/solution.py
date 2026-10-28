# Write your solution here. Read from stdin, write to stdout.

def can_achieve(foods, target, X):
    """
    Check if we can achieve at least 'target' units of each vitamin
    within X calories using dynamic programming.
    
    We'll use DP where dp[cal][v1][v2][v3] = True if we can achieve
    exactly (cal, v1, v2, v3) combination.
    
    But since vitamins can be large (up to N * 200000), we need a different approach.
    We'll use DP with states: dp[cal][v1][v2] = maximum v3 achievable
    """
    # Separate foods by vitamin type
    foods_by_vitamin = [[], [], []]
    for v, a, c in foods:
        foods_by_vitamin[v - 1].append((a, c))
    
    # For each vitamin, find minimum calories to get at least target units
    min_cal = [float('inf')] * 3
    
    for v_idx in range(3):
        # DP: dp[cal] = maximum vitamin units achievable with exactly cal calories
        dp = [0] * (X + 1)
        
        for amount, cal in foods_by_vitamin[v_idx]:
            # Traverse backwards to avoid using same item twice
            for c in range(X, cal - 1, -1):
                dp[c] = max(dp[c], dp[c - cal] + amount)
        
        # Find minimum calories to get at least target units
        for cal in range(X + 1):
            if dp[cal] >= target:
                min_cal[v_idx] = cal
                break
    
    # Check if we can achieve all three targets within X calories
    return min_cal[0] + min_cal[1] + min_cal[2] <= X


def solve():
    N, X = map(int, input().split())
    foods = []
    for _ in range(N):
        v, a, c = map(int, input().split())
        foods.append((v, a, c))
    
    # Binary search on the answer
    # Maximum possible answer is limited by sum of all vitamin amounts
    left, right = 0, 2 * 10**5 * N
    
    answer = 0
    
    while left <= right:
        mid = (left + right) // 2
        if can_achieve(foods, mid, X):
            answer = mid
            left = mid + 1
        else:
            right = mid - 1
    
    print(answer)

solve()
