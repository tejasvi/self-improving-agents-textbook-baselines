from collections import deque, defaultdict
from itertools import combinations


def is_connected(n, edges):
    """Check if a graph with n vertices and given edges is connected."""
    if not edges:
        return n == 1
    
    # Build adjacency list
    adj = defaultdict(set)
    vertices_in_edges = set()
    
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
        vertices_in_edges.add(u)
        vertices_in_edges.add(v)
    
    # Check if all vertices are used
    if len(vertices_in_edges) < n:
        return False
    
    # BFS from vertex 0
    visited = set()
    queue = deque([0])
    visited.add(0)
    
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if v not in visited:
                visited.add(v)
                queue.append(v)
    
    return len(visited) == n


def get_distances(n, edges):
    """Get distances from vertex 0 to all other vertices using BFS."""
    # Build adjacency list
    adj = defaultdict(set)
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    
    # BFS from vertex 0
    distances = [-1] * n
    distances[0] = 0
    queue = deque([0])
    
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if distances[v] == -1:
                distances[v] = distances[u] + 1
                queue.append(v)
    
    return distances


def check_balanced_distances(n, distances):
    """
    Check if the number of vertices at even distance equals 
    the number at odd distance from vertex 0.
    """
    even_count = 0
    odd_count = 0
    
    for i in range(n):
        if distances[i] == -1:
            # Not reachable (shouldn't happen in connected graph)
            return False
        elif distances[i] % 2 == 0:
            even_count += 1
        else:
            odd_count += 1
    
    return even_count == odd_count


def solve(n, p):
    """Solve the problem for given N and prime P."""
    # Generate all possible edges
    all_edges = []
    for i in range(n):
        for j in range(i + 1, n):
            all_edges.append((i, j))
    
    max_edges = len(all_edges)
    min_edges = n - 1  # minimum for connected graph
    
    results = []
    
    # For each possible number of edges M
    for m in range(min_edges, max_edges + 1):
        count = 0
        
        # Iterate through all combinations of m edges
        for edge_combo in combinations(all_edges, m):
            # Check if connected
            if not is_connected(n, edge_combo):
                continue
            
            # Check if balanced distances
            distances = get_distances(n, edge_combo)
            if check_balanced_distances(n, distances):
                count += 1
        
        results.append(count % p)
    
    return results


def main():
    n, p = map(int, input().split())
    results = solve(n, p)
    print(' '.join(map(str, results)))


if __name__ == '__main__':
    main()
