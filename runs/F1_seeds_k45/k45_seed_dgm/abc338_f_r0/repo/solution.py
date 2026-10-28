import sys
from collections import defaultdict
import heapq

def solve():
    N, M = map(int, input().split())
    
    # Build adjacency list
    graph = defaultdict(list)
    for _ in range(M):
        u, v, w = map(int, input().split())
        graph[u].append((v, w))
    
    # DP with bitmask and Dijkstra
    # dp[mask][v] = minimum cost to visit all vertices in mask and end at v
    INF = float('inf')
    dp = [[INF] * (N + 1) for _ in range(1 << N)]
    
    # Try starting from each vertex
    for start in range(1, N + 1):
        # Initialize: start from vertex 'start'
        mask = 1 << (start - 1)
        dp[mask][start] = 0
        
        # Use priority queue for Dijkstra-like approach
        pq = [(0, mask, start)]
        visited = set()
        
        while pq:
            cost, current_mask, v = heapq.heappop(pq)
            
            if (current_mask, v) in visited:
                continue
            visited.add((current_mask, v))
            
            if cost > dp[current_mask][v]:
                continue
            
            # Try to extend to all neighbors
            for neighbor, weight in graph[v]:
                new_mask = current_mask | (1 << (neighbor - 1))
                new_cost = cost + weight
                
                if new_cost < dp[new_mask][neighbor]:
                    dp[new_mask][neighbor] = new_cost
                    heapq.heappush(pq, (new_cost, new_mask, neighbor))
    
    # Find minimum cost to visit all vertices
    full_mask = (1 << N) - 1
    result = min(dp[full_mask])
    
    if result == INF:
        print("No")
    else:
        print(result)

solve()
