# Write your solution here. Read from stdin, write to stdout.

from collections import defaultdict
import heapq

def solve():
    N, M = map(int, input().split())
    
    # Build adjacency list
    graph = [[] for _ in range(N + 1)]
    
    for _ in range(M):
        u, v, w = map(int, input().split())
        graph[u].append((v, w))
    
    # Check if all vertices are reachable from any starting point
    def can_reach_all_from(start):
        visited = set()
        queue = [start]
        visited.add(start)
        while queue:
            u = queue.pop(0)
            for v, _ in graph[u]:
                if v not in visited:
                    visited.add(v)
                    queue.append(v)
        return len(visited) == N
    
    # Check if there exists a vertex from which all others are reachable
    valid_start = False
    for i in range(1, N + 1):
        if can_reach_all_from(i):
            valid_start = True
            break
    
    if not valid_start:
        print("No")
        return
    
    # Use Dijkstra with state (mask, vertex)
    # dist[mask][v] = minimum cost to reach state (mask, v)
    INF = float('inf')
    dist = [[INF] * (N + 1) for _ in range(1 << N)]
    
    # Priority queue: (cost, mask, vertex)
    pq = []
    
    # Initialize: start from each vertex
    for start in range(1, N + 1):
        mask = 1 << (start - 1)
        dist[mask][start] = 0
        heapq.heappush(pq, (0, mask, start))
    
    while pq:
        cost, mask, u = heapq.heappop(pq)
        
        if cost > dist[mask][u]:
            continue
        
        # Try extending to adjacent vertices
        for v, w in graph[u]:
            new_mask = mask | (1 << (v - 1))
            new_cost = cost + w
            
            if new_cost < dist[new_mask][v]:
                dist[new_mask][v] = new_cost
                heapq.heappush(pq, (new_cost, new_mask, v))
    
    # Find minimum cost among all states that visit all vertices
    full_mask = (1 << N) - 1
    ans = min(dist[full_mask])
    
    if ans == INF:
        print("No")
    else:
        print(ans)

solve()
