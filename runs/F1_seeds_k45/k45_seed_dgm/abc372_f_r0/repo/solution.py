def solve():
    MOD = 998244353
    
    # Read input
    N, M, K = map(int, input().split())
    
    # Build adjacency list for the graph
    # Each vertex i (1-indexed) has edges to:
    # 1. Next vertex in the cycle (i % N + 1)
    # 2. Additional edges from the M extra edges
    
    adj = [[] for _ in range(N + 1)]  # adj[i] contains all vertices reachable from vertex i
    
    # Add the cycle edges (edges 1 to N)
    for i in range(1, N + 1):
        next_vertex = i % N + 1
        adj[i].append(next_vertex)
    
    # Add the additional edges (edges N+1 to N+M)
    for _ in range(M):
        x, y = map(int, input().split())
        adj[x].append(y)
    
    # DP: dp[v] = number of ways to reach vertex v after current number of moves
    dp = [0] * (N + 1)
    dp[1] = 1  # Start at vertex 1
    
    # For each move
    for move in range(K):
        new_dp = [0] * (N + 1)
        
        # For each current vertex v with dp[v] > 0
        for v in range(1, N + 1):
            if dp[v] > 0:
                # Move to each adjacent vertex
                for next_v in adj[v]:
                    new_dp[next_v] = (new_dp[next_v] + dp[v]) % MOD
        
        dp = new_dp
    
    # Sum all ways to reach any vertex after K moves
    result = sum(dp[1:]) % MOD
    print(result)

solve()
