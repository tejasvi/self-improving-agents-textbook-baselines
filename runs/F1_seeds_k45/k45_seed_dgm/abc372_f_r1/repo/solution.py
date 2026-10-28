from collections import defaultdict

MOD = 998244353

# Read input
N, M, K = map(int, input().split())

# Build adjacency list
adj = defaultdict(list)

# Add the basic cycle edges: i -> i+1 (N -> 1)
for i in range(1, N + 1):
    next_vertex = (i % N) + 1
    adj[i].append(next_vertex)

# Add the M extra edges
for _ in range(M):
    x, y = map(int, input().split())
    adj[x].append(y)

# DP: dp[v] = number of ways to reach vertex v
# We use two arrays: current and next
curr = [0] * (N + 1)
curr[1] = 1  # Start at vertex 1

# Process K steps
for step in range(K):
    next_dp = [0] * (N + 1)
    
    # For each vertex with non-zero ways to reach it
    for v in range(1, N + 1):
        if curr[v] > 0:
            # From vertex v, we can go to any neighbor
            for neighbor in adj[v]:
                next_dp[neighbor] = (next_dp[neighbor] + curr[v]) % MOD
    
    curr = next_dp

# Sum all ways to reach any vertex after K steps
result = sum(curr[1:]) % MOD
print(result)
