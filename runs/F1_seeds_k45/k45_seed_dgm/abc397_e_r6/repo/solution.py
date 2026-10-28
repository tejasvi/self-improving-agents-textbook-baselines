from collections import defaultdict

def solve():
    N, K = map(int, input().split())
    NK = N * K
    
    # Build adjacency list
    adj = defaultdict(list)
    for _ in range(NK - 1):
        u, v = map(int, input().split())
        adj[u].append(v)
        adj[v].append(u)
    
    # Try to find N paths of length K each
    used_vertices = [False] * (NK + 1)
    used_edges = set()
    
    def is_valid_path(path):
        """Check if a path exists in the tree using only unused edges"""
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            edge = tuple(sorted([u, v]))
            if edge in used_edges:
                return False
            if v not in adj[u]:
                return False
        return True
    
    def add_path(path):
        """Add a path to the solution"""
        for vertex in path:
            used_vertices[vertex] = True
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            used_edges.add(tuple(sorted([u, v])))
    
    def remove_path(path):
        """Remove a path from the solution"""
        for vertex in path:
            used_vertices[vertex] = False
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            used_edges.discard(tuple(sorted([u, v])))
    
    def find_paths_from(start):
        """Find all possible paths of length K starting from a vertex"""
        result = []
        
        def dfs(path):
            if len(path) == K:
                result.append(path[:])
                return
            
            if len(path) == 0:
                current = start
            else:
                current = path[-1]
            
            for neighbor in adj[current]:
                if used_vertices[neighbor]:
                    continue
                
                edge = tuple(sorted([current, neighbor]))
                if edge in used_edges:
                    continue
                
                path.append(neighbor)
                dfs(path)
                path.pop()
        
        dfs([start])
        return result
    
    def backtrack(path_count):
        """Backtrack to find N paths"""
        if path_count == N:
            # Check if all vertices are used
            return all(used_vertices[1:NK + 1])
        
        # Find first unused vertex
        start = -1
        for i in range(1, NK + 1):
            if not used_vertices[i]:
                start = i
                break
        
        if start == -1:
            return False
        
        # Try all possible paths starting from this vertex
        possible_paths = find_paths_from(start)
        
        for path in possible_paths:
            add_path(path)
            if backtrack(path_count + 1):
                return True
            remove_path(path)
        
        return False
    
    if backtrack(0):
        print("Yes")
    else:
        print("No")

solve()
