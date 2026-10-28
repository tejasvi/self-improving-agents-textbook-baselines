import math

def euclidean_distance(x1, y1, x2, y2):
    """Calculate Euclidean distance between two points"""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def solve():
    n = int(input())
    checkpoints = []
    for _ in range(n):
        x, y = map(int, input().split())
        checkpoints.append((x, y))
    
    # dp[i] = minimum cost to reach checkpoint i
    # where cost = distance traveled + penalty for skipped checkpoints
    dp = [float('inf')] * n
    dp[0] = 0  # Starting at checkpoint 1 with no cost
    
    for i in range(1, n):
        # Try coming from any previous checkpoint j
        for j in range(i):
            # If we go directly from j to i, we skip (i - j - 1) checkpoints
            skipped = i - j - 1
            
            # Calculate penalty for skipping
            if skipped > 0:
                penalty = 2 ** (skipped - 1)
            else:
                penalty = 0
            
            # Calculate distance from checkpoint j to checkpoint i
            x1, y1 = checkpoints[j]
            x2, y2 = checkpoints[i]
            distance = euclidean_distance(x1, y1, x2, y2)
            
            # Total cost to reach checkpoint i via checkpoint j
            cost = dp[j] + distance + penalty
            
            # Update minimum cost
            dp[i] = min(dp[i], cost)
    
    # The answer is the minimum cost to reach the last checkpoint (N)
    result = dp[n - 1]
    print(f"{result:.17f}")

solve()
