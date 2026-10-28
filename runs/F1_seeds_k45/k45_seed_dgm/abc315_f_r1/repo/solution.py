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
    # We must start at checkpoint 0 and end at checkpoint n-1
    dp = [float('inf')] * n
    dp[0] = 0  # Starting at checkpoint 1 (index 0) with no penalty
    
    # For each checkpoint i
    for i in range(1, n):
        # Try coming from each previous checkpoint j
        for j in range(i):
            # Cost to go from checkpoint j to checkpoint i
            distance = euclidean_distance(checkpoints[j], checkpoints[i])
            
            # Number of checkpoints skipped between j and i
            skipped = i - j - 1
            
            # Penalty for skipping checkpoints
            penalty = 0
            if skipped > 0:
                penalty = 2 ** (skipped - 1)
            
            # Total cost to reach i via j
            cost = dp[j] + distance + penalty
            dp[i] = min(dp[i], cost)
    
    # The answer is the minimum cost to reach checkpoint n-1
    print(dp[n-1])

solve()
