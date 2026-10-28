from collections import deque, defaultdict
from itertools import combinations

def read_input():
    line = input().strip()
    N, P = map(int, line.split())
    return N, P

def is_connected(n, edges):
    """Check if graph is connected using BFS"""
    if not edges:
        return n == 1
    
    adj = defaultdict(set)
    vertices = set(range(1, n + 1))
    
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
        vertices.add(u)
        vertices.add(v)
    
    # If not all vertices appear in edges, graph is disconnected
    if len(vertices) < n:
        return False
    
    # BFS from vertex 1
    visited = {1}
    queue = deque([1])
    
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if v not in visited:
                visited.add(v)
                queue.append(v)
    
    return len(visited) == n

def check_distance_parity(n, edges):
    """
    Check if vertices with even and odd distance from vertex 1 are equal in count.
    Returns True if equal, False otherwise.
    """
    adj = defaultdict(set)
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    
    distance = [-1] * (n + 1)
    distance[1] = 0
    
    queue = deque([1])
    even_count = 1  # vertex 1 has distance 0 (even)
    odd_count = 0
    
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if distance[v] == -1:
                distance[v] = distance[u] + 1
                if distance[v] % 2 == 0:
                    even_count += 1
                else:
                    odd_count += 1
                queue.append(v)
    
    return even_count == odd_count

def count_graphs(n, p):
    """Count connected graphs for each edge count"""
    max_edges = n * (n - 1) // 2
    min_edges = n - 1
    
    # Generate all possible edges
    all_edges = list(combinations(range(1, n + 1), 2))
    total_possible = len(all_edges)
    
    # Count graphs for each edge count
    counts = [0] * (max_edges + 1)
    
    # Iterate through all possible subsets of edges
    # This is exponential but necessary to check all graphs
    for mask in range(1 << total_possible):
        edges = []
        for i in range(total_possible):
            if mask & (1 << i):
                edges.append(all_edges[i])
        
        m = len(edges)
        
        # Only check relevant edge counts
        if m < min_edges or m > max_edges:
            continue
        
        # Check if connected
        if not is_connected(n, edges):
            continue
        
        # Check if distance parities are balanced
        if check_distance_parity(n, edges):
            counts[m] += 1
    
    # Return counts for edges from min_edges to max_edges
    result = [counts[m] % p for m in range(min_edges, max_edges + 1)]
    return result

def main():
    n, p = read_input()
    
    result = count_graphs(n, p)
    
    print(' '.join(map(str, result)))

if __name__ == '__main__':
    main()
