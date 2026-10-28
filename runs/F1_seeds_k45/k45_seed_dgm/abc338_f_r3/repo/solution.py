# Write your solution here. Read from stdin, write to stdout.

def solve():
    N, M = map(int, input().split())
    
    # Build adjacency list with weights
    edges = [[] for _ in range(N + 1)]
    
    for _ in range(M):
        u, v, w = map(int, input().split())
        edges[u].append((v, w))
    
    # dp[v][mask] = minimum cost to be at vertex v with visited set = mask
    INF = float('inf')
    
    # Initialize DP table
    dp = [[INF] * (1 << N) for _ in range(N + 1)]
    
    all_visited = (1 << N) - 1
    
    # Try all starting vertices
    for start in range(1, N + 1):
        start_mask = 1 << (start - 1)
        dp[start][start_mask] = 0
    
    # Relax edges multiple times (Bellman-Ford style)
    # We need enough iterations to explore all possible paths
    for iteration in range(N * (1 << N)):
        updated = False
        for v in range(1, N + 1):
            for mask in range(1 << N):
                if dp[v][mask] == INF:
                    continue
                
                current_cost = dp[v][mask]
                
                # Try all outgoing edges from v
                for next_v, weight in edges[v]:
                    next_bit = next_v - 1
                    new_mask = mask | (1 << next_bit)
                    new_cost = current_cost + weight
                    
                    if new_cost < dp[next_v][new_mask]:
                        dp[next_v][new_mask] = new_cost
                        updated = True
        
        if not updated:
            break
    
    # Find minimum cost among all vertices with all visited
    result = INF
    for v in range(1, N + 1):
        result = min(result, dp[v][all_visited])
    
    if result == INF:
        print("No")
    else:
        print(result)

solve()
