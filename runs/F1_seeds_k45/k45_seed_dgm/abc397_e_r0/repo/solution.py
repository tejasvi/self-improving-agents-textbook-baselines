from collections import defaultdict

def solve():
    N, K = map(int, input().split())
    
    # Build adjacency list
    graph = defaultdict(list)
    total_vertices = N * K
    
    for _ in range(total_vertices - 1):
        u, v = map(int, input().split())
        graph[u].append(v)
        graph[v].append(u)
    
    used_vertices = set()
    used_edges = set()
    
    def dfs_find_path(start, length, path, path_set):
        """Recursively find a path of exactly 'length' vertices starting from 'start'"""
        if length == 1:
            return path
        
        for neighbor in graph[start]:
            edge = tuple(sorted([start, neighbor]))
            if neighbor not in used_vertices and neighbor not in path_set and edge not in used_edges:
                path_set.add(neighbor)
                result = dfs_find_path(neighbor, length - 1, path + [neighbor], path_set)
                if result is not None:
                    return result
                path_set.remove(neighbor)
        
        return None
    
    def backtrack(num_paths_found):
        """Recursively try to find N paths"""
        if num_paths_found == N:
            # Check if all vertices are used
            return len(used_vertices) == total_vertices
        
        # Find all unvisited vertices, sorted by degree of remaining edges
        unvisited = [v for v in range(1, total_vertices + 1) if v not in used_vertices]
        
        if not unvisited:
            return False
        
        # Sort by number of unvisited adjacent edges (ascending)
        # Vertices with fewer options should be tried first
        def count_available_edges(v):
            return sum(1 for neighbor in graph[v] 
                      if tuple(sorted([v, neighbor])) not in used_edges)
        
        unvisited.sort(key=count_available_edges)
        
        # Try starting from each unvisited vertex
        for start in unvisited:
            # Try to build a path starting from this vertex
            path_set = {start}
            path = dfs_find_path(start, K, [start], path_set)
            if path is not None:
                # Add this path
                used_vertices.update(path)
                for i in range(len(path) - 1):
                    used_edges.add(tuple(sorted([path[i], path[i+1]])))
                
                # Recurse
                result = backtrack(num_paths_found + 1)
                
                # Backtrack
                if result:
                    return True
                
                used_vertices.difference_update(path)
                for i in range(len(path) - 1):
                    used_edges.discard(tuple(sorted([path[i], path[i+1]])))
        
        return False
    
    if backtrack(0):
        print("Yes")
    else:
        print("No")

solve()
