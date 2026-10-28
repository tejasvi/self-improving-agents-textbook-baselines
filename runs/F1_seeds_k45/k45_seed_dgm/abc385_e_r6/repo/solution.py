from collections import defaultdict, deque

def solve():
    n = int(input())
    
    if n == 0:
        print(0)
        return
    
    adj = defaultdict(list)
    
    for _ in range(n - 1):
        u, v = map(int, input().split())
        adj[u].append(v)
        adj[v].append(u)
    
    # Try each vertex as the root of the Snowflake Tree
    max_vertices = 0
    
    for root in range(1, n + 1):
        # For this root, try to find the maximum Snowflake Tree
        # We need to find x children of root, and for each child,
        # all its children must be leaves (have no children except in snowflake tree)
        
        # First, identify which vertices are adjacent to root
        root_children = adj[root]
        x = len(root_children)
        
        if x == 0:
            continue
        
        # For each possible value of x (from 1 to number of actual children)
        for num_x in range(1, x + 1):
            # Try different subsets of x children
            # But we want to maximize the result, so we should be greedy
            # For each child, count how many leaves it has
            
            child_leaf_counts = []
            for child in root_children:
                # Count leaves of this child
                # A leaf is a vertex that is only connected to its parent
                leaf_count = 0
                for grandchild in adj[child]:
                    if grandchild != root:  # Not the root itself
                        # Check if grandchild is a leaf (only connected to child)
                        if len(adj[grandchild]) == 1:
                            leaf_count += 1
                child_leaf_counts.append((child, leaf_count))
            
            # Sort by leaf count in descending order to be greedy
            child_leaf_counts.sort(key=lambda x: x[1], reverse=True)
            
            # Select top num_x children
            selected_children = child_leaf_counts[:num_x]
            
            # All selected children must have the same number of leaves
            if len(selected_children) == num_x:
                leaf_counts = [count for _, count in selected_children]
                if len(set(leaf_counts)) == 1:  # All same
                    y = leaf_counts[0]
                    vertices_in_tree = 1 + num_x + num_x * y
                    max_vertices = max(max_vertices, vertices_in_tree)
    
    # The answer is the minimum number of deletions
    print(n - max_vertices)

solve()
