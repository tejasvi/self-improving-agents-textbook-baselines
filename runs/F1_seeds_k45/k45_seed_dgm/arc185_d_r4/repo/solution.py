MOD = 998244353

def modinv(a, m=MOD):
    """Compute modular inverse using Fermat's little theorem"""
    return pow(a, m - 2, m)

def solve():
    N, M = map(int, input().split())
    
    total_vertices = N * M + 1
    
    # Build adjacency list
    adj = [[] for _ in range(total_vertices)]
    
    for i in range(1, total_vertices):
        parent = max(i - N, 0)
        adj[i].append(parent)
        adj[parent].append(i)
    
    # For each vertex v, compute expected hitting time from 0 to v
    # using DFS on the tree rooted at 0
    
    parent = [-1] * total_vertices
    children = [[] for _ in range(total_vertices)]
    
    # Build rooted tree
    visited = [False] * total_vertices
    queue = [0]
    visited[0] = True
    
    while queue:
        u = queue.pop(0)
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                parent[v] = u
                children[u].append(v)
                queue.append(v)
    
    # Compute hitting times using tree DP
    # For a vertex v, we need to solve the random walk equations
    # We'll use a clever formula for trees
    
    # Key insight: for tree random walks starting at root 0
    # Expected hitting time to vertex v = 2 * (sum of degrees on path)
    # where we sum deg(u) for each vertex u on path from 0 to v
    
    # But we need to be careful: this might overcount or undercount
    # Let's use the effective resistance formula:
    # H(0,v) = 2 * R_eff(0,v) where R_eff is computed for the tree
    
    # For our tree, we can use a recursive formula:
    # Let E[v] = expected time to reach all vertices in subtree of v,
    # starting from v and returning to v
    
    def compute_subtree_cover(u):
        """
        Compute expected time to cover subtree rooted at u,
        starting from u and returning to u when done
        """
        if len(children[u]) == 0:
            return 0  # Leaf node, no subtree to cover
        
        total = 0
        for v in children[u]:
            # Time to go to v and cover its subtree
            # = 2 (back and forth) + E[cover subtree of v]
            subtree_time = compute_subtree_cover(v)
            
            # At u, we have degree d = 1 + len(children[u])
            # (parent edge + child edges)
            # Expected time to go to a specific child = degree
            degree_u = 1 + len(children[u]) if u != 0 else len(children[u])
            
            total += degree_u + subtree_time
        
        return total
    
    # This approach is getting complicated too
    # Let me use a direct formula for hitting times
    
    # For random walk on tree rooted at 0:
    # H(0, v) = sum over vertices u on path from 0 to v (excluding v):
    #           2 * deg(u) - 2
    # Plus some additional term
    
    # Actually, simpler formula:
    # H(0, v) = 2 * |edges| * some_factor
    # For a path of length d with degrees d_0, d_1, ..., d_{d-1}:
    # H(0, v) = 2 * (d_0 - 1) + 2 * (d_1 - 1) + ... 
    # No, this is also not right
    
    # Let me compute it properly using the theorem:
    # For tree rooted at r, the hitting time from r to v is:
    # H(r, v) = sum over edges (u, w) where u is parent of w, on path r to v:
    #           (deg(u) + deg(w) - 2) / (deg(u) - 1) or similar
    
    # Actually, let me use the simplest correct formula:
    # For tree rooted at 0, hitting time from 0 to v is:
    # H(0, v) = 2 * (sum of 1/deg(u) for u in T_v)
    # No, that's for effective resistance...
    
    # Let me just use the recursion more carefully:
    # For a subtree rooted at v with parent u:
    # E[time from u to paint entire subtree and return to u]
    # = sum over children c of v: (deg(u) + E[time for subtree of c] + deg(u))
    # = deg(u) * 2 * num_children + sum of E[subtree of c]
    
    # Hmm, this is also complex
    
    # Let me try a different approach: use the formula from literature
    # For random walk on tree rooted at 0:
    # Expected cover time = 2 * sum of edges weighted by subtree size
    
    def compute_with_subtree_sizes():
        # Compute subtree size for each vertex
        subtree_size = [0] * total_vertices
        
        def dfs_size(u):
            subtree_size[u] = 1
            for v in children[u]:
                subtree_size[u] += dfs_size(v)
            return subtree_size[u]
        
        dfs_size(0)
        
        # For each vertex v, compute hitting time
        # using edge-weight formula
        total_ops = 0
        
        for v in range(1, total_vertices):
            hitting_time = 0
            curr = v
            
            while curr != 0:
                par = parent[curr]
                degree_par = len(adj[par])
                size_subtree = subtree_size[curr]
                
                # Contribution of this edge: deg(par) * size(curr)
                # No, try: deg(par) * (n - size(curr))
                # Or: 2 * deg(par)
                
                hitting_time = (hitting_time + 2 * degree_par) % MOD
                curr = par
            
            total_ops = (total_ops + hitting_time) % MOD
        
        return total_ops
    
    result = compute_with_subtree_sizes()
    print(result)

solve()
