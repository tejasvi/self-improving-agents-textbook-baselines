#!/usr/bin/env python3

from collections import defaultdict

def solve():
    n = int(input())
    
    if n < 3:
        print(0)
        return
    
    # Build adjacency list
    adj = defaultdict(list)
    for _ in range(n - 1):
        u, v = map(int, input().split())
        adj[u].append(v)
        adj[v].append(u)
    
    min_deletions = n - 1  # Maximum possible deletions
    
    def get_subtree_size(node, parent):
        """Get size of subtree rooted at node, with parent as the parent"""
        size = 1
        for neighbor in adj[node]:
            if neighbor != parent:
                size += get_subtree_size(neighbor, node)
        return size
    
    def get_descendants(node, parent):
        """Get list of immediate children and their subtree sizes"""
        children = []
        for neighbor in adj[node]:
            if neighbor != parent:
                size = get_subtree_size(neighbor, node)
                children.append((neighbor, size))
        return children
    
    # Try each vertex as the root
    for root in range(1, n + 1):
        children = get_descendants(root, -1)
        
        if not children:
            # root is isolated (only happens if n=1)
            continue
        
        # Try different values of x (number of intermediate children to keep)
        for x in range(1, len(children) + 1):
            # For this x, try different values of y (leaves per child)
            # Maximum y is bounded by the largest child subtree
            max_y = max(child[1] - 1 for child in children)
            
            for y in range(1, max_y + 1):
                # Count how many children can support y leaves
                valid_children_count = sum(1 for _, size in children if size >= 1 + y)
                
                if valid_children_count >= x:
                    # We can form a snowflake tree with these parameters
                    # Total nodes to keep: 1 (root) + x (children) + x*y (leaves)
                    kept_nodes = 1 + x + x * y
                    deletions = n - kept_nodes
                    min_deletions = min(min_deletions, deletions)
    
    print(min_deletions)

solve()
