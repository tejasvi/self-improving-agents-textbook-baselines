MOD = 998244353

def modinv(a, m=MOD):
    return pow(a, m - 2, m)

def solve(N, M):
    # The tree structure:
    # Vertex i connects to max(i - N, 0)
    # This creates a tree where:
    # - Vertices 1 to N are children of 0
    # - Vertices N+1 to 2N are children of 1 to N
    # - And so on, for M levels
    
    # For each vertex v, we need to compute the expected hitting time from 0
    # Using the formula: E[T_v] = sum of 2 * (subtree_size) for each edge on path
    
    total_expected = 0
    
    # Process vertices level by level
    # Level 0: vertex 0
    # Level 1: vertices 1 to N
    # Level 2: vertices N+1 to 2N
    # Level k: vertices (k-1)*N+1 to k*N
    
    for level in range(1, M + 1):
        start_vertex = (level - 1) * N + 1
        end_vertex = level * N
        
        # For each vertex in this level
        for v in range(start_vertex, end_vertex + 1):
            # Compute expected hitting time from 0 to v
            # Path from 0 to v passes through ancestors
            
            # Find path: v -> parent(v) -> parent(parent(v)) -> ... -> 0
            expected_hitting_time = 0
            current = v
            
            for _ in range(level):  # level edges on path
                parent = max(current - N, 0)
                
                # Count vertices in subtree rooted at current (going away from parent)
                # For vertex current with parent, the subtree includes:
                # - current itself
                # - all descendants of current that don't go through parent
                
                # Subtree rooted at current (not going to parent)
                # consists of vertices from (current's children) onwards
                
                # For a vertex at level L with N children each:
                # Subtree size = 1 (itself) + N (children) + N^2 (grandchildren) + ...
                #              = 1 + N + N^2 + ... + N^(M - L)
                #              = (N^(M - L + 1) - 1) / (N - 1)  if N > 1
                #              = M - L + 1  if N = 1
                
                current_level = (current - 1) // N if current > 0 else 0
                remaining_levels = M - current_level
                
                if N == 1:
                    subtree_size = remaining_levels + 1
                else:
                    # Sum of geometric series: 1 + N + N^2 + ... + N^remaining_levels
                    subtree_size = (pow(N, remaining_levels + 1, MOD) - 1) * modinv(N - 1) % MOD
                
                expected_hitting_time = (expected_hitting_time + 2 * subtree_size) % MOD
                current = parent
            
            total_expected = (total_expected + expected_hitting_time) % MOD
    
    return total_expected

N, M = map(int, input().split())
print(solve(N, M))
