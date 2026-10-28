MOD = 998244353

def solve():
    N, Q = map(int, input().split())
    A = [0] + [0] + list(map(int, input().split()))  # A[1] unused, A[2] onwards
    
    for _ in range(Q):
        u, v = map(int, input().split())
        
        # Calculate the sum of distances for this query
        total = count_total_distance(u, v, A, N)
        print(total)

def count_total_distance(u, v, A, N):
    """
    For each edge (i, P_i) with weight A_i, count how many of the (N-1)! trees
    have this edge on the path from u to v.
    
    Key insight: Edge (i, P_i) is on the path from u to v iff:
    - Exactly one of {u, v} is a descendant of i (in the tree where this edge exists)
    
    We count for each possible parent of i, in how many ways the remaining
    parent assignments result in the edge being on the path.
    """
    
    total = 0
    
    for i in range(2, N + 1):
        # For vertex i, count how many of the (N-1)! trees have edge (i, P_i) on path u->v
        count = count_edge_appearances(u, v, i, A, N)
        total = (total + A[i] * count) % MOD
    
    return total

def count_edge_appearances(u, v, i, A, N):
    """
    Count in how many of the (N-1)! tree configurations is the edge
    connecting vertex i to its parent on the path from u to v.
    
    Approach: For each choice of parent P_i for vertex i (from {1,...,i-1}),
    count how many complete parent assignments result in the edge being on the path.
    """
    
    # Brute force enumeration for now
    total_count = 0
    
    # Generate all possible parent sequences
    def generate_all_parents(n):
        if n == 2:
            for p2 in range(1, 2):
                yield [p2]
        else:
            for rest in generate_all_parents(n - 1):
                for pi in range(1, n):
                    yield rest + [pi]
    
    # For small N, enumerate all trees
    for parents_list in generate_all_parents(N):
        # parents_list[i-2] is the parent of vertex i (for i >= 2)
        P = {1: 0}  # root has no parent  
        for idx in range(2, N + 1):
            P[idx] = parents_list[idx - 2]
        
        # Check if edge (i, P[i]) is on path u->v
        if is_edge_on_path(u, v, i, P, A, N):
            total_count += 1
    
    return total_count

def is_edge_on_path(u, v, i, P, A, N):
    """Check if edge (i, P[i]) is on the path from u to v."""
    
    # Find ancestors of u
    ancestors_u = set()
    curr = u
    while curr != 0:
        ancestors_u.add(curr)
        curr = P.get(curr, 0)
    
    # Find ancestors of v
    ancestors_v = set()
    curr = v
    while curr != 0:
        ancestors_v.add(curr)
        curr = P.get(curr, 0)
    
    # Find LCA
    curr = v
    lca = None
    while curr != 0:
        if curr in ancestors_u:
            lca = curr
            break
        curr = P.get(curr, 0)
    
    # Edge (i, P[i]) is on path iff:
    # - i is on the path from u to v
    # This means i must be an ancestor of one endpoint but not the other (or be an endpoint itself)
    
    # Actually, simpler: i is on path u->v iff it's an ancestor of both u and v
    # and P[i] is an ancestor of both, but removing the edge (i, P[i]) would separate them
    
    # Even simpler: Check if i is on the unique path from u to v
    # This happens iff: i is ancestor of u AND ancestor of v AND ...
    # No wait, that's only if i is LCA or above.
    
    # The path from u to v goes: u -> ... -> LCA -> ... -> v
    # So i is on this path iff:
    # - i is ancestor of u (or i=u) AND i is ancestor of LCA (or i=LCA)
    # - OR i is ancestor of v (or i=v) AND i is ancestor of LCA (or i=LCA)
    
    # More concretely:
    # - If i is LCA: on path
    # - If i is between u and LCA: on path  
    # - If i is between v and LCA: on path
    # - Otherwise: not on path
    
    # To check: i is on path iff path from u to i exists and path from i to v exists
    # and path from u to i and path from i to v don't overlap except at i
    
    # Another way: i is on path u->v iff dist(u,i) + dist(i,v) = dist(u,v)
    
    dist_ui = distance_in_tree(u, i, P, A)
    dist_iv = distance_in_tree(i, v, P, A)
    dist_uv = distance_in_tree(u, v, P, A)
    
    return dist_ui + dist_iv == dist_uv

def distance_in_tree(u, v, P, A):
    """Calculate distance from u to v in tree with given parent pointers."""
    
    if u == v:
        return 0
    
    # Find path from u to root
    path_u = []
    curr = u
    while curr != 0:
        path_u.append(curr)
        curr = P.get(curr, 0)
    
    # Find path from v to root
    path_v = []
    curr = v
    while curr != 0:
        path_v.append(curr)
        curr = P.get(curr, 0)
    
    # Find LCA
    ancestors_u = set(path_u)
    lca = None
    for node in path_v:
        if node in ancestors_u:
            lca = node
            break
    
    # Distance = dist(u, lca) + dist(v, lca)
    dist = 0
    
    curr = u
    while curr != lca:
        dist += A[curr]
        curr = P[curr]
    
    curr = v
    while curr != lca:
        dist += A[curr]
        curr = P[curr]
    
    return dist

solve()
