from collections import deque, defaultdict
from itertools import combinations

def is_connected(n, edges):
    """Check if graph is connected using BFS from vertex 0"""
    if not edges:
        return n == 1
    
    adj = defaultdict(set)
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    
    visited = set([0])
    queue = deque([0])
    
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if v not in visited:
                visited.add(v)
                queue.append(v)
    
    return len(visited) == n

def check_distance_parity(n, edges):
    """
    Check if number of vertices at even distance from vertex 0
    equals number at odd distance
    """
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
    
    # Count vertices at even and odd distances
    even_count = sum(1 for d in distances if d != -1 and d % 2 == 0)
    odd_count = sum(1 for d in distances if d != -1 and d % 2 == 1)
    
    return even_count == odd_count

def solve(n, p):
    """
    For each number of edges M from n-1 to n*(n-1)//2,
    count connected graphs satisfying the distance parity condition.
    """
    # Generate all possible edges
    all_edges = []
    for i in range(n):
        for j in range(i + 1, n):
            all_edges.append((i, j))
    
    max_edges = n * (n - 1) // 2
    results = []
    
    # For each number of edges M
    for m in range(n - 1, max_edges + 1):
        count = 0
        
        # Enumerate all combinations of M edges
        for edges in combinations(all_edges, m):
            # Check if connected
            if not is_connected(n, edges):
                continue
            
            # Check distance parity condition
            if check_distance_parity(n, edges):
                count += 1
        
        results.append(count % p)
    
    return results

def main():
    n, p = map(int, input().split())
    results = solve(n, p)
    print(' '.join(map(str, results)))

if __name__ == "__main__":
    main()
