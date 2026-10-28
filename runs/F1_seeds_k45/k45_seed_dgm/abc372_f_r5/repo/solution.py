def solve():
    MOD = 998244353
    
    # Read input
    N, M, K = map(int, input().split())
    
    # Build adjacency list
    graph = [[] for _ in range(N + 1)]
    
    # Add the first N edges (cycle edges)
    for i in range(1, N + 1):
        next_vertex = i + 1 if i < N else 1
        graph[i].append(next_vertex)
    
    # Add the M extra edges
    for _ in range(M):
        x, y = map(int, input().split())
        graph[x].append(y)
    
    # DP: dp[v] = number of ways to reach vertex v after current number of moves
    dp = [0] * (N + 1)
    dp[1] = 1  # Start at vertex 1
    
    # Simulate K moves
    for move in range(K):
        new_dp = [0] * (N + 1)
        for v in range(1, N + 1):
            if dp[v] > 0:
                # From vertex v, we can go to any neighbor
                for next_v in graph[v]:
                    new_dp[next_v] = (new_dp[next_v] + dp[v]) % MOD
        dp = new_dp
    
    # Sum all ways to reach any vertex after K moves
    result = sum(dp[1:]) % MOD
    print(result)

solve()
