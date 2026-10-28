from collections import defaultdict

MOD = 998244353

def solve():
    N, M, K = map(int, input().split())
    
    # Build adjacency list
    # First, add the N cycle edges: i -> (i+1) mod N
    # (vertices are 1-indexed, so: i -> i+1 for i=1..N-1, N -> 1)
    adj = defaultdict(list)
    
    for i in range(1, N + 1):
        next_vertex = (i % N) + 1
        adj[i].append(next_vertex)
    
    # Add M extra edges
    for _ in range(M):
        x, y = map(int, input().split())
        adj[x].append(y)
    
    # DP: dp[v] = number of ways to reach vertex v after current number of steps
    dp = [0] * (N + 1)
    dp[1] = 1  # Start at vertex 1
    
    # Perform K steps
    for step in range(K):
        next_dp = [0] * (N + 1)
        
        # For each vertex, distribute its count to adjacent vertices
        for v in range(1, N + 1):
            if dp[v] > 0:
                for next_v in adj[v]:
                    next_dp[next_v] = (next_dp[next_v] + dp[v]) % MOD
        
        dp = next_dp
    
    # Sum all ways to reach any vertex after K steps
    result = sum(dp[1:]) % MOD
    print(result)

solve()
