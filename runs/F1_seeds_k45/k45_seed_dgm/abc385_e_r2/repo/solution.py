from collections import defaultdict

def solve():
    N = int(input())
    
    adj = defaultdict(list)
    for _ in range(N - 1):
        u, v = map(int, input().split())
        adj[u].append(v)
        adj[v].append(u)
    
    def count_max_leaves(node, parent):
        """
        Count the maximum number of leaves we can keep in the subtree rooted at node.
        When node is an internal node (not root), a leaf is a vertex that we keep
        in the subtree and would have degree 1 in the final structure.
        """
        # If node becomes a leaf itself (degree 1 in original tree when parent is removed)
        if len(adj[node]) == 1 and parent != -1:
            return 1
        
        # Otherwise, node will be an internal node
        # We can keep all vertices that become leaves in our selection
        leaves = 0
        for child in adj[node]:
            if child != parent:
                leaves += count_max_leaves(child, node)
        
        return leaves
    
    def try_root(root):
        """Try using 'root' as the root of the Snowflake Tree."""
        
        neighbors = adj[root]
        
        if len(neighbors) == 0:
            return float('inf')
        
        min_deletions = float('inf')
        
        # For each neighbor, count the maximum leaves in its subtree
        neighbor_data = []
        for neighbor in neighbors:
            max_leaves = count_max_leaves(neighbor, root)
            neighbor_data.append((neighbor, max_leaves))
        
        # Try different values of x (number of internal nodes to keep)
        for x in range(1, len(neighbors) + 1):
            # Try different values of y (number of leaves per internal node)
            # y must be achievable by at least x neighbors
            
            max_y = max([leaves for _, leaves in neighbor_data])
            
            for y in range(1, max_y + 1):
                # Count how many neighbors have at least y leaves
                valid_neighbors = [leaves for _, leaves in neighbor_data if leaves >= y]
                
                if len(valid_neighbors) >= x:
                    # We can form a snowflake tree with this root, x, and y
                    # We keep: 1 root + x internal nodes + x*y leaves
                    kept = 1 + x + x * y
                    deletions = N - kept
                    min_deletions = min(min_deletions, deletions)
        
        return min_deletions
    
    # Try each vertex as root
    answer = float('inf')
    for root in range(1, N + 1):
        deletions = try_root(root)
        answer = min(answer, deletions)
    
    print(answer)

solve()
