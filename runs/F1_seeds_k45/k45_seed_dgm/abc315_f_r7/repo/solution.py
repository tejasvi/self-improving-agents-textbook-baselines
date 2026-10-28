import math

def euclidean_distance(p1, p2):
    """Calculate Euclidean distance between two points"""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def solve():
    n = int(input())
    checkpoints = []
    for _ in range(n):
        x, y = map(int, input().split())
        checkpoints.append((x, y))
    
    # dp[i][c] = minimum distance to reach checkpoint i having skipped exactly c checkpoints
    # c ranges from 0 to n-2 (we visit checkpoint 1 and n, so at most n-2 can be skipped)
    dp = [[float('inf')] * (n - 1) for _ in range(n)]
    dp[0][0] = 0  # Starting at checkpoint 0 (1 in problem) with 0 skipped
    
    for i in range(1, n):
        for j in range(i):
            # Number of checkpoints skipped when going from j to i
            # We skip checkpoints j+1, j+2, ..., i-1, so count is i - j - 1
            num_skipped_in_gap = i - j - 1
            
            # Distance from checkpoint j to checkpoint i
            distance = euclidean_distance(checkpoints[j], checkpoints[i])
            
            # Update dp[i][c] from dp[j][c - num_skipped_in_gap]
            for c in range(n - 1):
                prev_c = c - num_skipped_in_gap
                if 0 <= prev_c < n - 1:
                    cost = dp[j][prev_c] + distance
                    dp[i][c] = min(dp[i][c], cost)
    
    # Find the minimum total cost
    # We must reach checkpoint n-1 (checkpoint N in problem)
    # For each possible number of skipped checkpoints c, add the penalty
    min_total = float('inf')
    for c in range(n - 1):
        if dp[n - 1][c] < float('inf'):
            if c > 0:
                penalty = 2 ** (c - 1)
            else:
                penalty = 0
            total = dp[n - 1][c] + penalty
            min_total = min(min_total, total)
    
    print(min_total)

solve()
