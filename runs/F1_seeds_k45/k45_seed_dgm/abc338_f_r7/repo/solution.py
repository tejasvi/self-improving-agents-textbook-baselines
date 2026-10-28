def solve():
    N, M = map(int, input().split())
    
    # Initialize distance matrix with infinity
    INF = float('inf')
    dist = [[INF] * N for _ in range(N)]
    
    # Distance from a vertex to itself is 0
    for i in range(N):
        dist[i][i] = 0
    
    # Read edges and build distance matrix
    for _ in range(M):
        u, v, w = map(int, input().split())
        u -= 1  # Convert to 0-indexed
        v -= 1
        dist[u][v] = min(dist[u][v], w)  # Handle multiple edges
    
    # Floyd-Warshall algorithm to compute shortest paths
    for k in range(N):
        for i in range(N):
            for j in range(N):
                if dist[i][k] != INF and dist[k][j] != INF:
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    
    # dp[mask][i] = minimum cost to visit vertices in mask and end at vertex i
    dp = [[INF] * N for _ in range(1 << N)]
    
    # We can start from any vertex
    for start in range(N):
        mask = 1 << start
        dp[mask][start] = 0
    
    # Fill DP table
    for mask in range(1 << N):
        for u in range(N):
            if dp[mask][u] == INF:
                continue
            if not (mask & (1 << u)):
                continue
            
            # Try to extend to vertex v
            for v in range(N):
                if dist[u][v] == INF:
                    continue
                
                new_mask = mask | (1 << v)
                new_cost = dp[mask][u] + dist[u][v]
                
                if new_cost < dp[new_mask][v]:
                    dp[new_mask][v] = new_cost
    
    # Answer is the minimum cost to visit all vertices
    full_mask = (1 << N) - 1
    answer = INF
    
    for v in range(N):
        answer = min(answer, dp[full_mask][v])
    
    if answer == INF:
        print("No")
    else:
        print(answer)

solve()
