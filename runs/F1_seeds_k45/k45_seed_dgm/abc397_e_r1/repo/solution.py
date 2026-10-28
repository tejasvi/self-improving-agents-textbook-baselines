from collections import defaultdict

def solve():
    N, K = map(int, input().split())
    
    # Build adjacency list
    graph = defaultdict(list)
    for _ in range(N * K - 1):
        u, v = map(int, input().split())
        graph[u].append(v)
        graph[v].append(u)
    
    total_vertices = N * K
    
    # Special case
    if N * K == 1:
        print("Yes")
        return
    
    # Try to decompose the tree into N paths of length K
    
    def find_all_paths(start, length, forbidden):
        """Find all paths of given length starting from start vertex"""
        
        if start in forbidden:
            return []
        
        if length == 1:
            return [[start]]
        
        # DFS to find all paths
        all_paths = []
        
        def dfs(v, path, visited):
            if len(path) == length:
                all_paths.append(path[:])
                return
            
            for neighbor in graph[v]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    path.append(neighbor)
                    dfs(neighbor, path, visited)
                    path.pop()
                    visited.remove(neighbor)
        
        visited = {start}
        dfs(start, [start], visited)
        
        return all_paths
    
    def backtrack(used_vertices, num_paths):
        if num_paths == N:
            # Check if all vertices are used
            return len(used_vertices) == total_vertices
        
        # Prune: check if remaining vertices can form paths
        remaining = total_vertices - len(used_vertices)
        if remaining != (N - num_paths) * K:
            return False
        
        # Find the smallest unused vertex to start a new path
        start = None
        for v in range(1, total_vertices + 1):
            if v not in used_vertices:
                start = v
                break
        
        if start is None:
            return False
        
        # Try all possible paths of length K starting from this vertex
        paths = find_all_paths(start, K, used_vertices)
        
        if not paths:
            return False
        
        for path in paths:
            new_used = used_vertices | set(path)
            
            if backtrack(new_used, num_paths + 1):
                return True
        
        return False
    
    if backtrack(set(), 0):
        print("Yes")
    else:
        print("No")

solve()
