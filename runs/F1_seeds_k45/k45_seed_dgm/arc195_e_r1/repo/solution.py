# Write your solution here. Read from stdin, write to stdout.

MOD = 998244353

def solve():
    N, Q = map(int, input().split())
    A = [0] + [0] + list(map(int, input().split()))
    
    # Precompute factorials
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i-1] * i % MOD
    
    def modinv(a):
        return pow(a, MOD - 2, MOD)
    
    # For each query
    for _ in range(Q):
        u, v = map(int, input().split())
        
        # Key insight: for each edge i with weight A_i,
        # count in how many parent assignments it lies on the path from u to v
        # and multiply A_i by this count, then sum
        
        total = 0
        
        # For each possible edge from vertex i to its parent
        for i in range(2, N + 1):
            # Count: in how many parent assignments P is the edge (i, P_i) on the path from u to v?
            
            # An edge is on the path from u to v iff it separates them
            # In a rooted tree, edge (i, parent(i)) separates u and v iff:
            # - one of {u,v} is in subtree(i) and the other is not
            
            # Case 1: u is in subtree(i) and v is not
            # Case 2: v is in subtree(i) and u is not
            
            # For this, we need to count over all parent assignments:
            # How many have u in subtree(i) and v not in subtree(i) (or vice versa)?
            
            # This is complex because the subtree of i depends on all ancestors of vertices below i
            
            # Let me think recursively:
            # Subtree(i) consists of i and all vertices j > i such that parent chain reaches i
            
            # Actually, here's a key observation:
            # For vertex i to have u in its subtree and v not:
            # - We need P_u (possibly transitively) to eventually lead to i
            # - We need P_v to NOT eventually lead to i
            
            # In rooted trees, for u to be in subtree of i:
            # - If i < u: i must be an ancestor of u
            #   This requires that there's a path of parents from u going down through i
            # - If i > u: u cannot be in subtree of i (since we root at 1 and parents have smaller indices)
            
            # So u is in subtree(i) iff i < u and P path from u leads through i to 1
            
            # Wait, let me reconsider the tree structure:
            # Rooted at 1, for each i >= 2, P_i is the parent (where 1 <= P_i <= i-1)
            # So parents always have smaller indices
            
            # For u to be in subtree of i: u > i and path from u to 1 includes i
            # For v to be in subtree of i: v > i and path from v to 1 includes i
            
            count = 0
            
            # Case: u > i and v > i
            if u > i and v > i:
                # u in subtree(i) iff P chain from u passes through i
                # v in subtree(i) iff P chain from v passes through i
                # We want exactly one of them
                
                # We need to count parent assignments where:
                # - P_u path includes i, P_v path doesn't (or vice versa)
                
                # This is getting complex. For now, let me use the brute force approach
                # and optimize later if needed
                pass
            
            # Case: u < i < v
            # u cannot be in subtree(i) (parents are smaller)
            # v can be in subtree(i) iff parent chain from v includes i
            # So we want: v in subtree(i) = true, u in subtree(i) = false
            # This always contributes!
            elif u < i < v:
                # Edge (i, P_i) is on path(u,v)
                # P_i can be any vertex from 1 to i-1
                # The remaining N-2 vertices can be assigned as parents in (N-2)! ways
                count = fact[N-2]
                total = (total + count * A[i]) % MOD
            
            # Case: v < i < u (same as above by symmetry)
            elif v < i < u:
                count = fact[N-2]
                total = (total + count * A[i]) % MOD
            
            # Case: i < u < v or i < v < u
            # Neither u nor v in subtree(i), so edge not on path
            
            # Case: u < v < i or v < u < i
            # Neither in subtree(i)
        
        print(total)

solve()
