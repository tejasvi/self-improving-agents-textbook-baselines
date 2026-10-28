import math

def euclidean_distance(p1, p2):
    """Calculate Euclidean distance between two points."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def solve():
    n = int(input())
    checkpoints = []
    for _ in range(n):
        x, y = map(int, input().split())
        checkpoints.append((x, y))
    
    # dp[i] = minimum cost to reach checkpoint i (0-indexed)
    dp = [float('inf')] * n
    dp[0] = 0  # Start at checkpoint 1 (index 0) with no cost
    
    # For each checkpoint i
    for i in range(1, n):
        # Try reaching checkpoint i from every previous checkpoint j
        for j in range(i):
            # Number of checkpoints skipped between j and i
            num_skipped = i - j - 1
            
            # Calculate penalty
            if num_skipped == 0:
                penalty = 0
            else:
                penalty = 2 ** (num_skipped - 1)
            
            # Distance from checkpoint j to checkpoint i
            distance = euclidean_distance(checkpoints[j], checkpoints[i])
            
            # Cost to reach checkpoint i via checkpoint j
            cost = dp[j] + distance + penalty
            
            # Update if this is better
            dp[i] = min(dp[i], cost)
    
    # The answer is the minimum cost to reach checkpoint N (index n-1)
    print(dp[n - 1])

solve()
