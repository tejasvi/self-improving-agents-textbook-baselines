# Write your solution here. Read from stdin, write to stdout.

MOD = 998244353

def solve():
    N, M, K = map(int, input().split())
    
    # Build the adjacency list
    adj = [[] for _ in range(N + 1)]
    
    # Add the cycle edges (1->2, 2->3, ..., N->1)
    for i in range(1, N + 1):
        next_vertex = (i % N) + 1
        adj[i].append(next_vertex)
    
    # Add the custom edges
    for _ in range(M):
        x, y = map(int, input().split())
        adj[x].append(y)
    
    # DP: dp[v] = number of ways to reach vertex v after current number of moves
    dp = [0] * (N + 1)
    dp[1] = 1  # Start at vertex 1
    
    # Perform K moves
    for move in range(K):
        new_dp = [0] * (N + 1)
        
        # For each vertex that we can currently be at
        for v in range(1, N + 1):
            if dp[v] > 0:
                # For each outgoing edge from v
                for next_v in adj[v]:
                    new_dp[next_v] = (new_dp[next_v] + dp[v]) % MOD
        
        dp = new_dp
    
    # Sum all ways to reach any vertex after K moves
    result = sum(dp[1:]) % MOD
    print(result)

solve()
