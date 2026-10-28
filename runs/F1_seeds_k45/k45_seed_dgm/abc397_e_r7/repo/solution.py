from collections import defaultdict

def solve():
    N, K = map(int, input().split())
    
    # Build adjacency list
    adj = defaultdict(list)
    total_vertices = N * K
    
    for _ in range(total_vertices - 1):
        u, v = map(int, input().split())
        adj[u].append(v)
        adj[v].append(u)
    
    def dfs(node, parent):
        """
        Returns dictionary: path_length -> count
        Where path_length is the number of vertices in a partial path in the subtree
        that extends to the parent node
        
        Returns None if decomposition is impossible
        """
        # Start with current node
        open_paths = defaultdict(int)
        open_paths[1] = 1
        
        for neighbor in adj[node]:
            if neighbor == parent:
                continue
            
            child_result = dfs(neighbor, node)
            if child_result is None:
                return None
            
            # Process child's open paths
            for length, count in child_result.items():
                complement = K - 1 - length
                
                if complement == 0:
                    # Child path + current node = complete path!
                    # We need to "consume" from open_paths[1]
                    if open_paths[1] >= count:
                        open_paths[1] -= count
                        if open_paths[1] == 0:
                            del open_paths[1]
                        # These count child paths are completed
                    else:
                        # Not enough current nodes to match with all child paths
                        remaining = count - open_paths[1]
                        open_paths[1] = 0
                        del open_paths[1]
                        # Extend remaining child paths
                        new_length = length + 1  # = K - 1 + 1 = K
                        if new_length == K:
                            # These become complete paths, but they're at the boundary
                            # They can't extend further
                            # This is a problem! We have paths that can't be completed or extended
                            return None
                elif complement > 0 and complement in open_paths and open_paths[complement] > 0:
                    # Match with existing open paths
                    matches = min(count, open_paths[complement])
                    open_paths[complement] -= matches
                    if open_paths[complement] == 0:
                        del open_paths[complement]
                    remaining = count - matches
                    if remaining > 0:
                        new_length = length + 1
                        if new_length < K:
                            open_paths[new_length] += remaining
                        elif new_length == K:
                            # Complete paths
                            pass
                else:
                    # Extend through node
                    new_length = length + 1
                    if new_length < K:
                        open_paths[new_length] += count
                    elif new_length == K:
                        # Complete paths
                        pass
        
        # Try to match remaining open paths
        changed = True
        while changed:
            changed = False
            lengths = sorted(open_paths.keys())
            
            for length in lengths:
                if length not in open_paths or open_paths[length] == 0:
                    continue
                
                complement = K - 1 - length
                
                if complement == length:
                    if open_paths[length] >= 2:
                        pairs = open_paths[length] // 2
                        open_paths[length] -= pairs * 2
                        if open_paths[length] == 0:
                            del open_paths[length]
                        changed = True
                        break
                elif complement > 0 and complement < K - 1 and complement in open_paths and open_paths[complement] > 0:
                    open_paths[length] -= 1
                    open_paths[complement] -= 1
                    if open_paths[length] == 0:
                        del open_paths[length]
                    if open_paths[complement] == 0:
                        del open_paths[complement]
                    changed = True
                    break
        
        return open_paths
    
    result = dfs(1, -1)
    
    if result is None or len(result) == 0:
        print("Yes")
    else:
        print("No")

solve()
