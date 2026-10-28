# Traveling Salesman Problem with negative weights
# We need to visit all vertices at least once with minimum total edge weight

def solve():
    N, M = map(int, input().split())
    
    # Compute shortest paths between all pairs using Floyd-Warshall algorithm
    # This handles negative weights (no negative cycles guaranteed)
    INF = float('inf')
    dist = [[INF] * N for _ in range(N)]
    
    # Initialize distances
    for i in range(N):
        dist[i][i] = 0
    
    # Read edges and build distance matrix
    for _ in range(M):
        u, v, w = map(int, input().split())
        u -= 1  # Convert to 0-indexed
        v -= 1
        dist[u][v] = min(dist[u][v], w)  # Handle multiple edges (keep minimum)
    
    # Floyd-Warshall algorithm to find shortest paths between all pairs
    for k in range(N):
        for i in range(N):
            for j in range(N):
                if dist[i][k] != INF and dist[k][j] != INF:
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    
    # DP with bitmask for TSP
    # dp[mask][v] = minimum cost to visit vertices in mask and end at vertex v
    # where mask is a bitmask representing which vertices have been visited
    
    dp = [[INF] * N for _ in range(1 << N)]
    
    # Initialize: start from each vertex with cost 0
    for v in range(N):
        dp[1 << v][v] = 0
    
    # Fill DP table by iterating through all masks
    for mask in range(1 << N):
        for v in range(N):
            if dp[mask][v] == INF:
                continue
            if not (mask & (1 << v)):
                continue
            
            # Try to go to next vertex u using shortest path from v to u
            for u in range(N):
                if dist[v][u] != INF:
                    new_mask = mask | (1 << u)
                    dp[new_mask][u] = min(dp[new_mask][u], dp[mask][v] + dist[v][u])
    
    # Find the minimum cost to visit all vertices
    full_mask = (1 << N) - 1
    result = min(dp[full_mask])
    
    if result == INF:
        print("No")
    else:
        print(result)

solve()
