MOD = 998244353

def solve():
    # Read input
    N, M, K = map(int, input().split())
    
    # Build adjacency list
    # First, add the N cycle edges
    graph = [[] for _ in range(N + 1)]
    
    for i in range(1, N + 1):
        next_vertex = (i % N) + 1
        graph[i].append(next_vertex)
    
    # Add M additional edges
    for _ in range(M):
        x, y = map(int, input().split())
        graph[x].append(y)
    
    # DP: dp[v] = number of ways to reach vertex v after current number of steps
    dp = [0] * (N + 1)
    dp[1] = 1  # Start at vertex 1
    
    # For each step from 1 to K
    for step in range(K):
        new_dp = [0] * (N + 1)
        
        # For each vertex with non-zero ways
        for v in range(1, N + 1):
            if dp[v] > 0:
                # Move to each neighbor
                for next_v in graph[v]:
                    new_dp[next_v] = (new_dp[next_v] + dp[v]) % MOD
        
        dp = new_dp
    
    # Sum all ways to reach any vertex after K steps
    result = sum(dp[1:]) % MOD
    print(result)

solve()
