from collections import defaultdict

def solve():
    N, K = map(int, input().split())
    
    # Build adjacency list
    graph = defaultdict(list)
    degrees = defaultdict(int)
    
    for _ in range(N * K - 1):
        u, v = map(int, input().split())
        graph[u].append(v)
        graph[v].append(u)
        degrees[u] += 1
        degrees[v] += 1
    
    # Count vertices with odd degree
    odd_degree_count = sum(1 for d in degrees.values() if d % 2 == 1)
    
    # For a tree to be decomposable into paths, we need exactly 2*N vertices of odd degree
    # (each path has 2 endpoints, and odd-degree vertices must be endpoints)
    if odd_degree_count != 2 * N:
        print("No")
        return
    
    # Now we need to check if we can actually form N disjoint paths of length K
    visited_edges = set()
    
    def dfs_path(start, max_length):
        """Try to construct a path of length max_length starting from start"""
        path = [start]
        current = start
        prev = -1
        
        while len(path) < max_length:
            # Find next unvisited edge
            found = False
            for next_node in graph[current]:
                edge = (min(current, next_node), max(current, next_node))
                if edge not in visited_edges and next_node != prev:
                    visited_edges.add(edge)
                    path.append(next_node)
                    prev = current
                    current = next_node
                    found = True
                    break
            
            if not found:
                break
        
        return path if len(path) == max_length else None
    
    # Try to build N paths of length K
    for _ in range(N):
        found_path = False
        
        # Try to find a starting vertex
        for v in range(1, N * K + 1):
            # Check if this vertex has unvisited edges
            has_unvisited = False
            for u in graph[v]:
                edge = (min(v, u), max(v, u))
                if edge not in visited_edges:
                    has_unvisited = True
                    break
            
            if has_unvisited:
                path = dfs_path(v, K)
                if path:
                    found_path = True
                    break
        
        if not found_path:
            print("No")
            return
    
    # Verify all edges are used
    total_edges = N * K - 1
    if len(visited_edges) != total_edges:
        print("No")
        return
    
    print("Yes")

solve()
