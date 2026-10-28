# Write your solution here. Read from stdin, write to stdout.

from collections import defaultdict

def solve():
    N = int(input())
    
    if N < 3:
        print(0)
        return
    
    # Build adjacency list
    graph = defaultdict(list)
    for _ in range(N - 1):
        u, v = map(int, input().split())
        graph[u].append(v)
        graph[v].append(u)
    
    min_deletions = N - 3  # Maximum possible deletions (keep at least 3 vertices)
    
    # Try each vertex as root
    for root in range(1, N + 1):
        # Build the tree rooted at this vertex
        children = defaultdict(list)
        
        def build_tree(v, parent):
            for u in graph[v]:
                if u != parent:
                    children[v].append(u)
                    build_tree(u, v)
        
        build_tree(root, -1)
        
        num_root_children = len(children[root])
        
        if num_root_children == 0:
            continue
        
        # For each child of root, count how many direct leaves it has
        child_leaf_counts = []
        for child in children[root]:
            direct_children = children[child]
            leaves_count = 0
            for grandchild in direct_children:
                if len(children[grandchild]) == 0:
                    leaves_count += 1
            child_leaf_counts.append(leaves_count)
        
        # Sort leaf counts in descending order
        child_leaf_counts.sort(reverse=True)
        
        # Try all possible values of x (number of internal nodes) and y (leaves per internal node)
        for x in range(1, num_root_children + 1):
            # For x internal nodes, max y is the x-th largest child's leaf count
            max_y = child_leaf_counts[x - 1]
            
            # y ranges from 1 to max_y
            for y in range(1, max_y + 1):
                # This configuration is valid
                # We keep: 1 root + x internal nodes + xy leaves
                kept = 1 + x + x * y
                deletions = N - kept
                min_deletions = min(min_deletions, deletions)
    
    print(min_deletions)

solve()
