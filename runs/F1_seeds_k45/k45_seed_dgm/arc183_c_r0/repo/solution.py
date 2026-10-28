MOD = 998244353

def solve():
    N, M = map(int, input().split())
    constraints = []
    for _ in range(M):
        L, R, X = map(int, input().split())
        constraints.append((L-1, R-1, X-1))  # Convert to 0-indexed
    
    # Use backtracking with constraint checking
    perm = [0] * N
    used = [False] * (N + 1)
    count = [0]
    
    def is_valid_partial():
        # Check constraints that are fully determined
        for L, R, X in constraints:
            # Check if all positions in [L, R] are filled
            all_filled = all(perm[i] != 0 for i in range(L, R+1))
            if all_filled:
                max_val = max(perm[L:R+1])
                if perm[X] == max_val:
                    return False
        return True
    
    def backtrack(pos):
        if pos == N:
            # Verify all constraints
            for L, R, X in constraints:
                max_val = max(perm[L:R+1])
                if perm[X] == max_val:
                    return
            count[0] += 1
            return
        
        for val in range(1, N+1):
            if not used[val]:
                perm[pos] = val
                used[val] = True
                
                # Early pruning: check if current partial assignment can violate constraints
                valid = True
                for L, R, X in constraints:
                    # Only check if all positions in range are filled
                    if all(perm[i] != 0 for i in range(L, R+1)):
                        max_val = max(perm[L:R+1])
                        if perm[X] == max_val:
                            valid = False
                            break
                
                if valid:
                    backtrack(pos + 1)
                
                perm[pos] = 0
                used[val] = False
    
    backtrack(0)
    print(count[0] % MOD)

solve()
