from collections import defaultdict

def solve():
    n = int(input())
    products = []
    for _ in range(n):
        products.append(input().strip())
    
    if n == 0:
        return 0
    
    # Build a directed graph where each product name is an edge
    graph = defaultdict(set)
    reverse_graph = defaultdict(set)
    in_degree = defaultdict(int)
    out_degree = defaultdict(int)
    
    for product in products:
        u, v = product[0], product[1]
        graph[u].add(v)
        reverse_graph[v].add(u)
        out_degree[u] += 1
        in_degree[v] += 1
    
    # Find all nodes that appear in the graph
    all_nodes = set()
    for product in products:
        all_nodes.add(product[0])
        all_nodes.add(product[1])
    
    # Find weakly connected components using DFS (treating as undirected)
    visited = set()
    components = []
    
    def dfs(node, component):
        visited.add(node)
        component.add(node)
        # Check outgoing edges
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor, component)
        # Check incoming edges
        for neighbor in reverse_graph[node]:
            if neighbor not in visited:
                dfs(neighbor, component)
    
    for node in all_nodes:
        if node not in visited:
            component = set()
            dfs(node, component)
            components.append(component)
    
    # For each component, calculate the number of paths needed
    total_paths = 0
    
    for component in components:
        # Count nodes with more outgoing than incoming edges
        extra_starts = 0
        for node in component:
            if out_degree[node] > in_degree[node]:
                extra_starts += 1
        
        if extra_starts == 0:
            # All nodes have equal in/out degree - Eulerian circuit
            total_paths += 1
        else:
            # Need extra_starts paths
            total_paths += extra_starts
    
    return total_paths

print(solve())
