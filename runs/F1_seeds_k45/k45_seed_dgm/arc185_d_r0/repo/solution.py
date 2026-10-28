MOD = 998244353

def modinv(a, m=MOD):
    """Modular inverse using Fermat's little theorem"""
    return pow(a, m - 2, m)

def solve():
    N, M = map(int, input().split())
    
    # Build adjacency list
    num_vertices = N * M + 1
    adj = [[] for _ in range(num_vertices)]
    
    for i in range(1, num_vertices):
        j = max(i - N, 0)
        adj[i].append(j)
        adj[j].append(i)
    
    # Remove duplicate neighbors
    for i in range(num_vertices):
        adj[i] = list(set(adj[i]))
    
    # For small inputs, use memoization
    if num_vertices <= 20:
        from functools import lru_cache
        
        @lru_cache(maxsize=None)
        def compute_expected(current, unpainted_mask):
            # current: current vertex
            # unpainted_mask: bitmask of unpainted vertices (excluding vertex 0)
            # returns: expected number of operations until all painted
            
            if unpainted_mask == 0:
                return 0
            
            neighbors = adj[current]
            degree = len(neighbors)
            
            if degree == 0:
                return 0
            
            expected = 0
            for neighbor in neighbors:
                # Move to neighbor and compute expected from there
                new_mask = unpainted_mask
                
                # Paint neighbor if it's unpainted (and not 0)
                if neighbor > 0 and (unpainted_mask & (1 << (neighbor - 1))):
                    new_mask = unpainted_mask & ~(1 << (neighbor - 1))
                
                expected += compute_expected(neighbor, new_mask)
            
            expected = expected * modinv(degree) % MOD
            expected = (expected + 1) % MOD
            
            return expected
        
        # Start at vertex 0 with all vertices 1..N*M unpainted
        initial_mask = (1 << (num_vertices - 1)) - 1
        result = compute_expected(0, initial_mask)
        print(result)
    else:
        # For larger inputs, derive a formula
        # The tree structure is: vertex i connects to max(i-N, 0)
        # This creates M levels
        
        # Let me think about this differently using linearity of expectation
        # and properties of random walks on trees
        
        # E[operations] = sum over all non-zero vertices v of E[visits to v]
        
        # For a random walk starting at root and visiting all vertices,
        # the expected number of visits to vertex v is related to its depth and subtree size
        
        # Using theory of random walks on trees:
        # E[visits to v] = O(depth_of_v * subtree_size_of_v) or similar
        
        # For this specific tree structure with levels and branching factor N,
        # we can compute the expected visits more carefully
        
        # Let's use a formula approach:
        # For each vertex, compute expected number of times it's visited
        
        # Tree structure:
        # Level 0: 1 vertex (vertex 0)
        # Level 1: N vertices (vertices 1 to N)
        # Level 2: N vertices (vertices N+1 to 2N)
        # ...
        # Level M: N vertices (vertices (M-1)*N + 1 to M*N)
        
        # For vertex at level i with subtree rooted at it:
        # Expected visits depends on how many times we must pass through it
        # to visit all descendants
        
        # By symmetry, all vertices at the same level with isomorphic subtrees
        # have the same expected visits
        
        # Let E[i] = expected visits to a vertex at level i
        # E[0] = 1 + sum of (expected times we return to 0)
        
        # For a random walk on a tree starting at root,
        # expected number of times we visit each non-root vertex is 
        # 2 * (number of times we must cross each edge to visit descendants)
        
        # Actually, let me use a cleaner approach:
        # Let f[v] = expected operations starting from v until all vertices are painted
        # f[v] = 1 + (1/deg[v]) * sum_{u in neighbors[v]} f[u]
        # But we need to handle the "already painted" vertices
        
        # For this problem, I think we need to compute the expected cover time
        # of a random walk starting at vertex 0
        
        # For a tree, the cover time can be computed using the formula:
        # E[cover] = sum over all vertices v of E[hitting time from 0 to v]
        
        # Hitting time from 0 to v in a tree:
        # H[0->v] = 2 * (sum of edge weights on path 0->v) 
        #         = 2 * (v in this case since all edges have weight 1)
        #         Actually for random walk: H[0->v] involves effective resistances
        
        # Let me try computing it differently using Gaussian elimination
        # for the linear system even for large N and M
        
        # The linear system is: for each non-zero vertex v:
        # E[v] = 1 + (1/deg[v]) * sum_{u adjacent to v} E[u]
        # with boundary condition: E[0] = 1 + (1/deg[0]) * sum E[u] for u adjacent to 0
        
        # All equations are coupled, so we solve:
        # (I - T) * E = 1 (vector of ones)
        # where T[v][u] = 1/deg[v] if u adjacent to v, 0 otherwise
        
        # For efficient computation with large N and M, we'd need
        # to exploit the tree structure (no cycles)
        
        # Let me implement a solution using Gaussian elimination
        # but optimized for sparse matrices (tree structure)
        
        # Build the system of equations
        # E[v] = 1 + (1/deg[v]) * sum_{u adjacent to v} E[u]
        # Rearrange: E[v] - (1/deg[v]) * sum_{u adjacent to v} E[u] = 1
        
        # Use Gaussian elimination with modular arithmetic
        
        n = num_vertices
        
        # Build augmented matrix [A | b] where A*E = b
        # A[v][u] = 1 if v==u, else -1/deg[v] if u adjacent to v, else 0
        # b[v] = 1
        
        # To avoid fractions, multiply row v by deg[v]:
        # deg[v]*E[v] - sum_{u adjacent to v} E[u] = deg[v]
        
        # Create matrix
        matrix = [[0] * (n + 1) for _ in range(n)]
        
        for v in range(n):
            deg_v = len(adj[v])
            if deg_v == 0:
                matrix[v][v] = 1
                matrix[v][n] = 0
            else:
                deg_inv = modinv(deg_v)
                matrix[v][v] = 1
                for u in adj[v]:
                    matrix[v][u] = (matrix[v][u] - deg_inv) % MOD
                matrix[v][n] = 1
        
        # Gaussian elimination
        for col in range(n):
            # Find pivot
            pivot_row = col
            for row in range(col + 1, n):
                if matrix[row][col] % MOD != 0:
                    pivot_row = row
                    break
            
            if matrix[pivot_row][col] % MOD == 0:
                continue
            
            # Swap rows
            matrix[col], matrix[pivot_row] = matrix[pivot_row], matrix[col]
            
            # Eliminate
            pivot_inv = modinv(matrix[col][col])
            for j in range(col, n + 1):
                matrix[col][j] = matrix[col][j] * pivot_inv % MOD
            
            for row in range(n):
                if row != col and matrix[row][col] != 0:
                    factor = matrix[row][col]
                    for j in range(col, n + 1):
                        matrix[row][j] = (matrix[row][j] - factor * matrix[col][j]) % MOD
        
        # Back substitution
        E = [0] * n
        for i in range(n):
            E[i] = matrix[i][n]
        
        # Sum up the expected operations
        # E[total] = sum of E[v] for all non-zero vertices
        result = sum(E[1:]) % MOD
        print(result)

solve()
