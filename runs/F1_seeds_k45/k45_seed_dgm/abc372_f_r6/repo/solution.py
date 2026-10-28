#!/usr/bin/env python3

MOD = 998244353

def solve():
    # Read input
    N, M, K = map(int, input().split())
    
    # Build adjacency list
    # First, add the cycle edges: i -> i+1 (with N -> 1)
    graph = [[] for _ in range(N + 1)]
    for i in range(1, N + 1):
        next_vertex = (i % N) + 1
        graph[i].append(next_vertex)
    
    # Add the additional M edges
    for _ in range(M):
        x, y = map(int, input().split())
        graph[x].append(y)
    
    # DP: dp[v] = number of ways to reach vertex v after current number of moves
    # We'll use two arrays to alternate between current and next state
    dp = [0] * (N + 1)
    dp[1] = 1  # Start at vertex 1
    
    # Perform K moves
    for move in range(K):
        new_dp = [0] * (N + 1)
        
        # For each vertex we can currently be at
        for v in range(1, N + 1):
            if dp[v] > 0:
                # Move to all adjacent vertices
                for next_v in graph[v]:
                    new_dp[next_v] = (new_dp[next_v] + dp[v]) % MOD
        
        dp = new_dp
    
    # Sum all ways to be at any vertex after K moves
    result = sum(dp[1:]) % MOD
    print(result)

solve()
