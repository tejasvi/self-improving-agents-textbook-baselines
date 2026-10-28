def solve():
    N, K = map(int, input().split())
    NK = N * K
    
    # Build adjacency list
    adj = [[] for _ in range(NK + 1)]
    for _ in range(NK - 1):
        u, v = map(int, input().split())
        adj[u].append(v)
        adj[v].append(u)
    
    # Track which vertices are used
    used = [False] * (NK + 1)
    paths_found = 0
    
    def dfs_extend_path(current, parent, path_length):
        """
        Try to extend a path from current vertex.
        Returns the path if we can extend it to length K, None otherwise.
        """
        if path_length == K:
            return [current]
        
        for next_vertex in adj[current]:
            if next_vertex == parent or used[next_vertex]:
                continue
            
            result = dfs_extend_path(next_vertex, current, path_length + 1)
            if result is not None:
                result.append(current)
                return result
        
        return None
    
    def try_build_paths():
        """Try to build N paths of length K greedily."""
        nonlocal paths_found
        paths_found = 0
        
        for start in range(1, NK + 1):
            if used[start]:
                continue
            
            # Try to build a path starting from 'start'
            found_path = False
            for neighbor in adj[start]:
                if used[neighbor]:
                    continue
                
                path = dfs_extend_path(neighbor, start, 2)
                if path is not None:
                    path.append(start)
                    if len(path) == K:
                        # Mark all vertices in path as used
                        for v in path:
                            used[v] = True
                        paths_found += 1
                        found_path = True
                        break
            
            if not found_path and not used[start]:
                # Could not form a path starting with this vertex
                return False
        
        return paths_found == N
    
    if try_build_paths():
        print("Yes")
    else:
        print("No")

solve()
