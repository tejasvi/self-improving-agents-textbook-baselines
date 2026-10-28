from itertools import combinations
from collections import deque

def bfs_distances(graph, start, n):
    """Compute distances from start vertex using BFS"""
    dist = [-1] * n
    dist[start] = 0
    queue = deque([start])
    
    while queue:
        u = queue.popleft()
        for v in graph[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                queue.append(v)
    
    return dist

def is_connected(graph, n):
    """Check if graph is connected"""
    dist = bfs_distances(graph, 0, n)
    return all(d != -1 for d in dist)

def check_odd_even(graph, n):
    """Check if equal number of vertices at even and odd distance from vertex 0"""
    dist = bfs_distances(graph, 0, n)
    
    even_count = sum(1 for d in dist if d % 2 == 0)
    odd_count = sum(1 for d in dist if d % 2 == 1)
    
    return even_count == odd_count

def solve(n, p):
    """Solve the problem for given N and P"""
    results = []
    
    # All possible edges (as pairs of vertex indices 0 to n-1)
    all_edges = list(combinations(range(n), 2))
    max_edges = len(all_edges)
    
    # For each number of edges from n-1 to n(n-1)/2
    min_edges = n - 1
    max_m = n * (n - 1) // 2
    
    for m in range(min_edges, max_m + 1):
        count = 0
        
        # Enumerate all combinations of m edges
        for edge_combo in combinations(all_edges, m):
            # Build adjacency list
            graph = [[] for _ in range(n)]
            for u, v in edge_combo:
                graph[u].append(v)
                graph[v].append(u)
            
            # Check if connected and satisfies the condition
            if is_connected(graph, n) and check_odd_even(graph, n):
                count += 1
        
        results.append(count % p)
    
    return results

# Read input
n, p = map(int, input().split())

# Solve and output
results = solve(n, p)
print(' '.join(map(str, results)))
