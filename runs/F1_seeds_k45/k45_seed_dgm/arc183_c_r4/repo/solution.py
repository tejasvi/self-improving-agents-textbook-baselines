MOD = 998244353

def solve():
    N, M = map(int, input().split())
    conditions = []
    for _ in range(M):
        L, R, X = map(int, input().split())
        conditions.append((L-1, R-1, X-1))  # Convert to 0-indexed
    
    count = 0
    
    def is_valid(perm, partial_len):
        """Check if current partial permutation can lead to a valid complete permutation"""
        # For conditions where range is completely filled, check if violated
        for L, R, X in conditions:
            if R < partial_len:  # Range [L, R] is completely filled
                max_val = max(perm[L:R+1])
                if max_val == perm[X]:
                    return False
        return True
    
    def backtrack(perm, used):
        nonlocal count
        
        if len(perm) == N:
            # Check all conditions
            valid = True
            for L, R, X in conditions:
                max_val = max(perm[L:R+1])
                if max_val == perm[X]:
                    valid = False
                    break
            if valid:
                count += 1
            return
        
        # Early termination if current state is invalid
        if not is_valid(perm, len(perm)):
            return
        
        # Try placing each unused number
        for num in range(1, N+1):
            if num not in used:
                perm.append(num)
                used.add(num)
                backtrack(perm, used)
                perm.pop()
                used.remove(num)
    
    backtrack([], set())
    print(count % MOD)

solve()
