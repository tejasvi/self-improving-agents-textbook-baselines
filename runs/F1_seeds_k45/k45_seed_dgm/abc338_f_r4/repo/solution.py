from collections import defaultdict

def solve():
    N, M = map(int, input().split())
    
    # Build adjacency list
    graph = defaultdict(list)  # graph[u] = [(v, w), ...]
    
    for _ in range(M):
        u, v, w = map(int, input().split())
        graph[u].append((v, w))
    
    # Use DP with bitmask: dp[mask][v] = minimum cost to visit vertices in mask and end at v
    INF = float('inf')
    dp = [[INF] * (N + 1) for _ in range(1 << N)]
    
    # Initialize: start from each vertex
    for start in range(1, N + 1):
        mask = 1 << (start - 1)
        dp[mask][start] = 0
    
    # Relaxation process - similar to Bellman-Ford but with bitmask
    # We need to relax edges multiple times to find optimal paths with negative weights
    for iteration in range((1 << N) * N):
        updated = False
        for mask in range(1, 1 << N):
            for v in range(1, N + 1):
                if dp[mask][v] == INF:
                    continue
                
                # Try to go to next vertex via each outgoing edge
                for next_v, weight in graph[v]:
                    next_mask = mask | (1 << (next_v - 1))
                    new_cost = dp[mask][v] + weight
                    if new_cost < dp[next_mask][next_v]:
                        dp[next_mask][next_v] = new_cost
                        updated = True
        
        if not updated:
            break
    
    # Find minimum cost to visit all vertices
    full_mask = (1 << N) - 1
    result = min(dp[full_mask][1:N+1])
    
    if result == INF:
        print("No")
    else:
        print(result)

solve()
