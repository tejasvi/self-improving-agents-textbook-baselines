import math

def euclidean_distance(p1, p2):
    """Calculate Euclidean distance between two points"""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def penalty(skipped_count):
    """Calculate penalty for skipping checkpoints"""
    if skipped_count > 0:
        return 2 ** (skipped_count - 1)
    else:
        return 0

def solve():
    n = int(input())
    checkpoints = []
    for _ in range(n):
        x, y = map(int, input().split())
        checkpoints.append((x, y))
    
    # dp[i] = minimum cost to reach checkpoint i
    dp = [float('inf')] * n
    dp[0] = 0  # Starting at checkpoint 1 (index 0), cost is 0
    
    # For each checkpoint i
    for i in range(1, n):
        # Try coming from each previous checkpoint j
        for j in range(i):
            # Distance from checkpoint j to checkpoint i
            dist = euclidean_distance(checkpoints[j], checkpoints[i])
            
            # Number of skipped checkpoints between j and i
            # If we go from checkpoint j to checkpoint i, we skip i-j-1 checkpoints
            skipped = i - j - 1
            
            # Total cost: previous cost + distance + penalty
            cost = dp[j] + dist + penalty(skipped)
            
            # Update dp[i] if this path is better
            dp[i] = min(dp[i], cost)
    
    # The answer is the minimum cost to reach checkpoint N (index n-1)
    print(dp[n-1])

solve()
