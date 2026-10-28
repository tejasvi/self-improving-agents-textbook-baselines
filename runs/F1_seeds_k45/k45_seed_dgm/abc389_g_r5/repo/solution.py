from itertools import combinations
from collections import deque

def read_input():
    """Read N and P from stdin"""
    line = input().split()
    N = int(line[0])
    P = int(line[1])
    return N, P

def bfs_check(adj, N, start=1):
    """
    Check if graph is connected and count vertices at even/odd distances.
    Returns (is_connected, even_count, odd_count) or (False, 0, 0) if not connected.
    """
    distances = [-1] * (N + 1)
    distances[start] = 0
    queue = deque([start])
    visited = 1
    
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if distances[v] == -1:
                distances[v] = distances[u] + 1
                visited += 1
                queue.append(v)
    
    # Check if connected
    if visited != N:
        return False, 0, 0
    
    # Count even and odd distances
    even_count = sum(1 for i in range(1, N + 1) if distances[i] % 2 == 0)
    odd_count = N - even_count
    
    return True, even_count, odd_count

def count_valid_graphs(N, M, P):
    """
    Count connected graphs with N vertices and M edges that satisfy the condition.
    """
    max_edges = N * (N - 1) // 2
    
    if M < N - 1 or M > max_edges:
        return 0
    
    # Generate all possible edges
    all_edges = list(combinations(range(1, N + 1), 2))
    
    if M > len(all_edges):
        return 0
    
    count = 0
    
    # Iterate through all combinations of M edges
    for edge_combination in combinations(all_edges, M):
        # Build adjacency list
        adj = [[] for _ in range(N + 1)]
        for u, v in edge_combination:
            adj[u].append(v)
            adj[v].append(u)
        
        # Check if connected and satisfies condition
        is_connected, even_count, odd_count = bfs_check(adj, N, start=1)
        
        if is_connected and even_count == odd_count:
            count += 1
    
    return count % P

def main():
    N, P = read_input()
    
    max_edges = N * (N - 1) // 2
    min_edges = N - 1
    
    results = []
    for M in range(min_edges, max_edges + 1):
        count = count_valid_graphs(N, M, P)
        results.append(str(count))
    
    print(' '.join(results))

if __name__ == "__main__":
    main()
