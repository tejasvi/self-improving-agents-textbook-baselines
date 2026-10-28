def solve():
    N, K = map(int, input().split())
    NK = N * K
    
    # Build adjacency list
    adj = [[] for _ in range(NK + 1)]
    for _ in range(NK - 1):
        u, v = map(int, input().split())
        adj[u].append(v)
        adj[v].append(u)
    
    path_count = [0]  # Count of completed paths
    
    def dfs(u, parent):
        """
        Returns the length of the open path extending from this subtree to parent.
        Returns -1 if decomposition is invalid.
        """
        # Get all open paths from children
        open_paths = []
        
        for v in adj[u]:
            if v == parent:
                continue
            
            child_result = dfs(v, u)
            if child_result == -1:
                return -1  # Invalid in subtree
            
            if child_result > 0:
                open_paths.append(child_result)
        
        # Now at node u, we have open_paths coming from children
        # Each value is the number of edges in an open path
        # We need to pair them up: if two paths of length a and b meet at u,
        # and a + b == K - 1, then they form a complete path of K edges
        
        # Try to match pairs greedily
        remaining = []
        i = 0
        while i < len(open_paths):
            found_pair = False
            for j in range(i + 1, len(open_paths)):
                if open_paths[i] + open_paths[j] == K - 1:
                    # Match them - they form a complete path
                    path_count[0] += 1
                    open_paths[j] = -1  # Mark as matched
                    found_pair = True
                    break
            
            if not found_pair:
                remaining.append(open_paths[i])
            else:
                open_paths[i] = -1
            i += 1
        
        # What to return?
        if len(remaining) == 0:
            # No open path to extend - this node by itself becomes an endpoint
            # OR no children at all (leaf)
            # Return 0 means no open path (this node can be an endpoint)
            # Actually, if this is a leaf, we need to return 1 (edge from here to parent)
            # But we already handled that - at a leaf, adj[u] only has parent
            # So remaining will be empty, return 1 for the edge to parent
            return 1
        elif len(remaining) == 1:
            # One open path continues
            path_len = remaining[0]
            # This path will continue to parent, adding 1 edge (u to parent)
            new_len = path_len + 1
            
            # Check if it becomes exactly K
            if new_len > K:
                return -1  # Invalid - path too long
            elif new_len == K:
                # Path is complete! Return 0 (no open path continues)
                path_count[0] += 1
                return 0
            else:
                # Path continues with length new_len
                return new_len
        else:
            # More than 1 remaining path - can't all pass to parent
            return -1
    
    result = dfs(1, -1)
    
    # Check validity
    if result == -1:
        print("No")
    elif result != 1:
        # At root, we should have no open path (result should be 1 for the non-existent edge to parent)
        # Actually, at root there's no parent, so we shouldn't have any open path
        # Hmm, this is confusing
        print("No")
    elif path_count[0] != N:
        print("No")
    else:
        print("Yes")

solve()
