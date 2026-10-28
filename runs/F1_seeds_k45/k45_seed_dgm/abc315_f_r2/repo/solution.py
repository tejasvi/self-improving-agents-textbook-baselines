import math

def solve():
    n = int(input())
    checkpoints = []
    for _ in range(n):
        x, y = map(int, input().split())
        checkpoints.append((x, y))
    
    # Calculate Euclidean distance between two checkpoints
    def distance(i, j):
        x1, y1 = checkpoints[i]
        x2, y2 = checkpoints[j]
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    
    # dp[i] = minimum cost to reach checkpoint i (visiting checkpoint i)
    dp = [float('inf')] * n
    dp[0] = 0  # Start at checkpoint 1 (index 0) with no cost
    
    # For each checkpoint i
    for i in range(1, n):
        # Try all possible previous checkpoints j < i
        for j in range(i):
            # Number of checkpoints skipped between j and i
            skipped = i - j - 1
            
            # Calculate penalty
            if skipped > 0:
                penalty = 2 ** (skipped - 1)
            else:
                penalty = 0
            
            # Cost to go from j to i
            dist = distance(j, i)
            cost = dp[j] + dist + penalty
            
            # Update dp[i]
            dp[i] = min(dp[i], cost)
    
    # The answer is the minimum cost to reach checkpoint N (index n-1)
    print(dp[n - 1])

solve()
