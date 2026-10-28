from collections import defaultdict, deque

def solve():
    N = int(input())
    
    if N == 1:
        print(0)
        return
    
    adj = defaultdict(list)
    for _ in range(N - 1):
        u, v = map(int, input().split())
        adj[u].append(v)
        adj[v].append(u)
    
    min_deletions = N  # worst case: delete all but 1
    
    # Try each vertex as root
    for root in range(1, N + 1):
        # Count leaves in each subtree rooted at children of root
        for x in range(1, len(adj[root]) + 1):
            # For each possible number of intermediate vertices
            result = try_root_and_x(root, x, adj, N)
            if result is not None:
                deletions = N - result
                min_deletions = min(min_deletions, deletions)
    
    print(min_deletions)

def count_leaves_in_subtree(v, parent, adj, blocked_children=None):
    """Count leaves in subtree rooted at v, not going through blocked_children"""
    if blocked_children is None:
        blocked_children = set()
    
    # Check if v is a leaf
    unblocked_neighbors = [u for u in adj[v] if u != parent and u not in blocked_children]
    if not unblocked_neighbors:
        return 1
    
    total = 0
    for u in unblocked_neighbors:
        total += count_leaves_in_subtree(u, v, adj, blocked_children)
    return total

def count_subtree_size(v, parent, adj, blocked_children=None):
    """Count vertices in subtree rooted at v, not going through blocked_children"""
    if blocked_children is None:
        blocked_children = set()
    
    unblocked_neighbors = [u for u in adj[v] if u != parent and u not in blocked_children]
    total = 1
    for u in unblocked_neighbors:
        total += count_subtree_size(u, v, adj, blocked_children)
    return total

def try_root_and_x(root, x, adj, N):
    """Try using 'root' as root and 'x' as number of intermediate vertices"""
    children = adj[root]
    if len(children) < x:
        return None
    
    # Try all combinations of x children
    from itertools import combinations
    
    best_kept = 0
    
    for child_combo in combinations(children, x):
        # For this combination, check if we can make a valid snowflake tree
        # Each child must have at least 1 leaf in its subtree
        leaf_counts = []
        subtree_sizes = []
        
        blocked = set(adj[root]) - set(child_combo)
        
        for child in child_combo:
            leaves = count_leaves_in_subtree(child, root, adj, blocked)
            size = count_subtree_size(child, root, adj, blocked)
            leaf_counts.append(leaves)
            subtree_sizes.append(size)
        
        # Check if all children have the same number of leaves y
        if len(set(leaf_counts)) == 1:
            y = leaf_counts[0]
            # We can keep: 1 root + x children + x*y leaves
            kept = 1 + x + x * y
            best_kept = max(best_kept, kept)
    
    if best_kept > 0:
        return best_kept
    return None

solve()
