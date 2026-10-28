MOD = 998244353

def solve():
    N, M = map(int, input().split())
    conditions = []
    for _ in range(M):
        L, R, X = map(int, input().split())
        conditions.append((L-1, R-1, X-1))  # Convert to 0-indexed
    
    # Count valid permutations using backtracking
    count = 0
    
    def is_valid_permutation(perm):
        """Check if a complete permutation satisfies all conditions"""
        for L, R, X in conditions:
            max_val = max(perm[L:R+1])
            if max_val == perm[X]:
                return False
        return True
    
    def backtrack(perm, available):
        """Generate permutations and count valid ones"""
        nonlocal count
        
        if len(perm) == N:
            if is_valid_permutation(perm):
                count += 1
            return
        
        # Try each available number
        for num in sorted(available):
            perm.append(num)
            new_available = available - {num}
            backtrack(perm, new_available)
            perm.pop()
    
    backtrack([], set(range(1, N+1)))
    print(count % MOD)

solve()
