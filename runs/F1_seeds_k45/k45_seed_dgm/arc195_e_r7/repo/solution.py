MOD = 998244353

def solve():
    N, Q = map(int, input().split())
    A = [0] + [0] + list(map(int, input().split()))  # A[i] is weight of edge from i to parent
    
    # Precompute factorials
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % MOD
    
    for _ in range(Q):
        u, v = map(int, input().split())
        
        # For each edge i (from 2 to N), count how many tree configurations have this edge on path u->v
        total = 0
        
        for i in range(2, N + 1):
            # Edge i connects i to its parent P_i
            # This edge is on the path from u to v if:
            # - i is on the unique path from u to v in some tree
            # - This depends on whether i is an ancestor of u or v
            
            # For edge i to be on path u->v:
            # Case 1: i is ancestor of u but not v
            # Case 2: i is ancestor of v but not u
            # Case 3: i is ancestor of both u and v, and removing i disconnects them
            
            # Actually, we need to count: in how many trees is i on the path?
            # i is on path u->v iff i is on the unique path in the tree
            # This is complex because it depends on the entire tree structure
            
            # Better approach: for each subset of vertices that could form the path,
            # count configurations where that path is realized
            pass
        
        print(total)

solve()
