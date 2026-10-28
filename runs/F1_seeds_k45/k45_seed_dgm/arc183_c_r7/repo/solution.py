#!/usr/bin/env python3

MOD = 998244353

def solve():
    N, M = map(int, input().split())
    constraints = []
    for _ in range(M):
        L, R, X = map(int, input().split())
        constraints.append((L-1, R-1, X-1))  # Convert to 0-indexed
    
    def is_valid_complete(perm):
        # Check all constraints on a complete permutation
        for L, R, X in constraints:
            max_in_range = max(perm[L:R+1])
            if max_in_range == perm[X]:
                return False
        return True
    
    # Backtracking to count valid permutations
    count = 0
    
    def backtrack(pos, perm, used):
        nonlocal count
        
        if pos == N:
            if is_valid_complete(perm):
                count += 1
            return
        
        for val in range(N):
            if not used[val]:
                perm[pos] = val
                used[val] = True
                
                # Early pruning: check constraints that are now complete
                valid = True
                for L, R, X in constraints:
                    if R < pos:
                        # This constraint range is completely filled
                        max_in_range = max(perm[L:R+1])
                        if max_in_range == perm[X]:
                            valid = False
                            break
                    elif R == pos and X < pos:
                        # Range is now complete and X was before
                        max_in_range = max(perm[L:R+1])
                        if max_in_range == perm[X]:
                            valid = False
                            break
                
                if valid:
                    backtrack(pos + 1, perm, used)
                
                perm[pos] = -1
                used[val] = False
    
    perm = [-1] * N
    used = [False] * N
    backtrack(0, perm, used)
    
    print(count % MOD)

solve()
