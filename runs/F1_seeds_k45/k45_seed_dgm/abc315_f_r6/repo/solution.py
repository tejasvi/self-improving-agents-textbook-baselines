import math
import sys

n = int(sys.stdin.readline())
checkpoints = []
for _ in range(n):
    x, y = map(int, sys.stdin.readline().split())
    checkpoints.append((x, y))

def distance(i, j):
    x1, y1 = checkpoints[i]
    x2, y2 = checkpoints[j]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# dp[i] = minimum cost to reach checkpoint i
dp = [float('inf')] * n
dp[0] = 0

for i in range(1, n):
    for j in range(i):
        num_skipped = i - j - 1
        
        if num_skipped == 0:
            penalty = 0
        else:
            penalty = 2 ** (num_skipped - 1)
        
        cost = dp[j] + distance(j, i) + penalty
        dp[i] = min(dp[i], cost)

print(dp[n - 1])
