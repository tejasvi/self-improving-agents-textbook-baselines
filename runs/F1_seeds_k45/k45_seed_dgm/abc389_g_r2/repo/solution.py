from collections import deque, defaultdict
from itertools import combinations

def read_input():
    line = input().strip().split()
    N = int(line[0])
    P = int(line[1])
    return N, P

def is_connected(n, edges):
    """Check if graph with n vertices and given edges is connected"""
    if not edges:
        return n <= 1
    
    adj = defaultdict(list)
    vertices = set()
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
        vertices.add(u)
        vertices.add(v)
    
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

def get_distances(n, edges):
    """Get shortest distances from vertex 1 to all other vertices using BFS"""
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    
    distances = [-1] * (n + 1)
    distances[1] = 0
    queue = deque([1])
    
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if distances[v] == -1:
                distances[v] = distances[u] + 1
                queue.append(v)
    
    return distances

def satisfies_condition(n, edges):
    """Check if the graph satisfies the even/odd distance condition"""
    distances = get_distances(n, edges)
    
    # Count vertices at even and odd distances
    even_count = 0
    odd_count = 0
    
    for i in range(1, n + 1):
        if distances[i] == -1:  # Not reachable (not connected)
            return False
        if distances[i] % 2 == 0:
            even_count += 1
        else:
            odd_count += 1
    
    return even_count == odd_count == n // 2

def solve(N, P):
    """Solve the problem"""
    max_edges = N * (N - 1) // 2
    results = []
    
    # Generate all possible edges
    all_vertices = list(range(1, N + 1))
    all_possible_edges = list(combinations(all_vertices, 2))
    
    # For each number of edges M from N-1 to max_edges
    for M in range(N - 1, max_edges + 1):
        count = 0
        
        # Generate all combinations of M edges
        for edges in combinations(all_possible_edges, M):
            # Check if connected
            if not is_connected(N, edges):
                continue
            
            # Check if satisfies the condition
            if satisfies_condition(N, edges):
                count += 1
        
        results.append(count % P)
    
    return results

def main():
    N, P = read_input()
    results = solve(N, P)
    print(' '.join(map(str, results)))

if __name__ == "__main__":
    main()
