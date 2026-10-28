import math
import sys

def distance(p1, p2):
    """Calculate Euclidean distance between two points"""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def solve():
    n = int(input())
    checkpoints = []
    for _ in range(n):
        x, y = map(int, input().split())
        checkpoints.append((x, y))
    
    # dp[i][c] = minimum distance to reach checkpoint i with exactly c checkpoints skipped
    # c is the count of skipped checkpoints from the start
    INF = float('inf')
    
    # Maximum possible skipped checkpoints is n-2 (all except first and last)
    dp = [[INF] * (n - 1) for _ in range(n)]
    
    # Start at checkpoint 0 (index 0)
    dp[0][0] = 0
    
    # Fill DP table
    for i in range(n):
        for skipped in range(n - 1):
            if dp[i][skipped] == INF:
                continue
            
            # Try to go to checkpoint j (where j > i)
            for j in range(i + 1, n):
                # Number of checkpoints we're skipping by going from i to j
                skip_count = j - i - 1
                new_skipped = skipped + skip_count
                
                if new_skipped >= n - 1:
                    continue
                
                dist = distance(checkpoints[i], checkpoints[j])
                new_cost = dp[i][skipped] + dist
                
                dp[j][new_skipped] = min(dp[j][new_skipped], new_cost)
    
    # Find the minimum total cost
    min_total = INF
    
    for skipped in range(n - 1):
        if dp[n - 1][skipped] == INF:
            continue
        
        # Calculate penalty
        if skipped == 0:
            penalty = 0
        else:
            penalty = 2 ** (skipped - 1)
        
        total_cost = dp[n - 1][skipped] + penalty
        min_total = min(min_total, total_cost)
    
    print(f"{min_total:.17f}")

solve()
