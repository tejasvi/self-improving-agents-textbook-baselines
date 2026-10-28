#!/usr/bin/env python3
from collections import deque
from itertools import combinations

def bfs_distances(n, adj_list):
    """BFS to find distances from vertex 0"""
    dist = [-1] * n
    dist[0] = 0
    queue = deque([0])
    
    while queue:
        u = queue.popleft()
        for v in adj_list[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                queue.append(v)
    
    return dist

def is_connected_and_check_parity(n, edges):
    """
    Check if graph is connected and satisfies parity condition.
    Returns True if both conditions are met.
    """
    if not edges:
        return False
    
    # Build adjacency list
    adj_list = [[] for _ in range(n)]
    for u, v in edges:
        adj_list[u].append(v)
        adj_list[v].append(u)
    
    # Check connectivity and compute distances simultaneously
    dist = bfs_distances(n, adj_list)
    
    # Check if connected
    if any(d == -1 for d in dist):
        return False
    
    # Check parity condition
    even_count = sum(1 for d in dist if d % 2 == 0)
    odd_count = sum(1 for d in dist if d % 2 == 1)
    
    return even_count == odd_count

def solve(n, p):
    # All possible edges as pairs (i, j) where i < j
    all_edges = [(i, j) for i in range(n) for j in range(i+1, n)]
    max_edges = len(all_edges)
    min_edges = n - 1
    
    results = []
    
    # For each number of edges M
    for m in range(min_edges, max_edges + 1):
        count = 0
        # Generate all combinations of m edges
        for edge_set in combinations(all_edges, m):
            if is_connected_and_check_parity(n, edge_set):
                count = (count + 1) % p
        
        results.append(count)
    
    return results

def main():
    n, p = map(int, input().split())
    results = solve(n, p)
    print(' '.join(map(str, results)))

if __name__ == "__main__":
    main()
