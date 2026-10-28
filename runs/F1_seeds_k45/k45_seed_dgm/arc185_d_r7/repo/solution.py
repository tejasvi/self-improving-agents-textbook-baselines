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
    
    # Compute tree properties using DFS
    visited = [False] * total_vertices
    depth = [0] * total_vertices
    parent_arr = [0] * total_vertices
    subtree_size = [0] * total_vertices
    
    def dfs_setup(v, p, d):
        visited[v] = True
        parent_arr[v] = p
        depth[v] = d
        subtree_size[v] = 1
        
        for u in adj[v]:
            if not visited[u]:
                dfs_setup(u, v, d + 1)
                subtree_size[v] += subtree_size[u]
    
    dfs_setup(0, -1, 0)
    
    # Expected total number of operations
    # = sum over all unpainted vertices v of (expected hitting time from 0 to v)
    
    # For a random walk on a tree, the expected hitting time from node u to node v is:
    # The sum of degrees along edges we need to traverse
    
    # More precisely: 
    # E[u->v] = 2 * (number of nodes reachable from v in the direction away from u)
    # when considering random walk returning to u before finally reaching v
    
    # For a rooted tree at 0:
    # E[0->v] = 2 * (sum of |subtree(u)| - 1) for each ancestor u of v
    # This counts the expected "work" to reach each level
    
    total = 0
    
    for v in range(1, total_vertices):
        # Compute expected hitting time from 0 to v
        # E[0->v] = degree of each ancestor we need to pass through
        
        current = v
        expected_time = 0
        
        # Walk from v to root, accumulating expected times
        while current != 0:
            p = parent_arr[current]
            
            # At node p, to reach child current:
            # - We have deg(p) choices at random
            # - Probability of choosing current is 1/deg(p)
            # - Expected time to successfully choose current is deg(p)
            # But we also need to account for paths that don't lead directly there
            
            # The correct formula for expected hitting time from p to direct child c:
            # E[p->c] = deg(p) (when c is a direct child)
            # Because: E = 1 + (deg(p)-1)/deg(p) * E
            #          => E * deg(p) = deg(p) + (deg(p)-1) * E
            #          => E = deg(p)
            
            deg_p = len(adj[p])
            expected_time += deg_p
            
            current = p
        
        total += expected_time
    
    # Modular arithmetic
    result = total % MOD
    print(result)

solve()
