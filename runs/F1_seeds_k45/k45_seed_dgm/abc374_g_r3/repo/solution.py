# Write your solution here. Read from stdin, write to stdout.

from collections import defaultdict

def solve():
    n = int(input())
    edges = []
    for _ in range(n):
        s = input().strip()
        edges.append((s[0], s[1]))
    
    # Build graph
    in_degree = defaultdict(int)
    out_degree = defaultdict(int)
    graph = defaultdict(set)  # adjacency list for connectivity
    
    for u, v in edges:
        out_degree[u] += 1
        in_degree[v] += 1
        graph[u].add(v)
        graph[v].add(u)
    
    # Get all vertices that are in the graph
    all_vertices = set()
    for u, v in edges:
        all_vertices.add(u)
        all_vertices.add(v)
    
    # Find weakly connected components
    visited = set()
    components = []
    
    def dfs(node, component):
        visited.add(node)
        component.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor, component)
    
    for vertex in all_vertices:
        if vertex not in visited:
            component = set()
            dfs(vertex, component)
            components.append(component)
    
    num_components = len(components)
    
    # For each component, count vertices with out_degree > in_degree
    # The minimum paths needed = sum over all components of max(1, num_sources_in_component)
    total_paths = 0
    
    for component in components:
        sources = 0
        for v in component:
            if out_degree[v] > in_degree[v]:
                sources += 1
        # Each component needs at least 1 path
        # But if there are sources (out > in), we need at least that many
        total_paths += max(1, sources)
    
    print(total_paths)

solve()
