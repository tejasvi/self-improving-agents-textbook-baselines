# Write your solution here. Read from stdin, write to stdout.

def solve():
    N, K = map(int, input().split())
    
    # Build adjacency list
    edges = []
    adj = [[] for _ in range(N * K + 1)]
    
    for _ in range(N * K - 1):
        u, v = map(int, input().split())
        adj[u].append(v)
        adj[v].append(u)
        edges.append((u, v))
    
    # Try to decompose the tree into N paths of length K
    # Use DFS-based approach
    
    total_vertices = N * K
    visited = [False] * (total_vertices + 1)
    path_count = [0]  # Use list to allow modification in nested function
    
    def dfs(node, parent, path_length):
        """
        Try to build a path starting from node.
        Returns (success, remaining_path_length, next_node)
        If remaining_path_length == 0, we've completed a path
        Otherwise, returns the node where path continues
        """
        visited[node] = True
        path_length += 1
        
        if path_length == K:
            # Path complete
            path_count[0] += 1
            return True, 0, -1
        
        # Try to continue path to an unvisited neighbor
        for neighbor in adj[node]:
            if not visited[neighbor]:
                success, remaining, next_node = dfs(neighbor, node, path_length)
                if success and remaining == 0:
                    return True, 0, -1
                if success:
                    return True, remaining, next_node
        
        # Cannot continue path, return current state
        return False, path_length, node
    
    # Try starting DFS from each unvisited node
    for start in range(1, total_vertices + 1):
        if not visited[start]:
            success, remaining, _ = dfs(start, -1, 0)
            if not success or remaining > 0:
                print("No")
                return
    
    if path_count[0] == N:
        print("Yes")
    else:
        print("No")

solve()
