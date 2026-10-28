from collections import defaultdict, deque

def read_input():
    n = int(input())
    edges = []
    graph = defaultdict(list)
    for _ in range(n - 1):
        u, v = map(int, input().split())
        edges.append((u, v))
        graph[u].append(v)
        graph[v].append(u)
    return n, edges, graph

def count_leaves_in_subtree(v, parent, graph):
    """Count the number of leaf nodes in subtree rooted at v"""
    children = [u for u in graph[v] if u != parent]
    if not children:
        return 1  # v is a leaf
    
    total = 0
    for child in children:
        total += count_leaves_in_subtree(child, v, graph)
    return total

def get_subtree_size(v, parent, graph):
    """Get the number of vertices in subtree rooted at v"""
    size = 1
    for child in graph[v]:
        if child != parent:
            size += get_subtree_size(child, v, graph)
    return size

def is_valid_snowflake_subtree(v, parent, graph, expected_y):
    """
    Check if the subtree rooted at v (when coming from parent) is a valid
    "leaf structure" - i.e., v has expected_y leaf children and no other children.
    Returns True if valid, False otherwise.
    """
    children = [u for u in graph[v] if u != parent]
    
    # All children should be leaves
    if len(children) != expected_y:
        return False
    
    for child in children:
        # Each child should be a leaf (have no further children except v)
        if len(graph[child]) != 1:
            return False
    
    return True

def count_deletions_for_root_and_x_y(root, x, y, graph, N):
    """
    Count vertices to delete if we use 'root' as the snowflake root,
    keep exactly x children, and each child has exactly y leaves.
    """
    children = graph[root]
    
    if len(children) < x:
        return float('inf')
    
    # Try all combinations of x children
    from itertools import combinations
    min_deletions = float('inf')
    
    for selected_children in combinations(children, x):
        # Check if these selected children can be valid snowflake children
        valid = True
        for child in selected_children:
            if not is_valid_snowflake_subtree(child, root, graph, y):
                valid = False
                break
        
        if valid:
            # Count total vertices in the snowflake tree
            total_in_snowflake = 1 + x + x * y  # root + x children + x*y leaves
            deletions = N - total_in_snowflake
            min_deletions = min(min_deletions, deletions)
    
    return min_deletions

def solve(N, edges, graph):
    min_deletions = N - 1  # worst case: keep only a root
    
    # Try each vertex as root
    for root in range(1, N + 1):
        children = graph[root]
        
        # Skip if root has no children
        if not children:
            continue
        
        # Try different values of x (number of children to keep)
        for x in range(1, len(children) + 1):
            # Try different values of y (number of leaves per child)
            # y can be at most the minimum degree among the selected children
            max_y = min(len(graph[child]) - 1 for child in children)
            
            for y in range(1, max_y + 1):
                deletions = count_deletions_for_root_and_x_y(root, x, y, graph, N)
                min_deletions = min(min_deletions, deletions)
    
    return min_deletions

# Main
N, edges, graph = read_input()
print(solve(N, edges, graph))
