MOD = 998244353

def solve():
    N, M = map(int, input().split())
    constraints = []
    for _ in range(M):
        L, R, X = map(int, input().split())
        constraints.append((L - 1, R - 1, X - 1))  # Convert to 0-indexed
    
    # Check if a complete permutation satisfies all constraints
    def is_valid(perm):
        for L, R, X in constraints:
            max_val = max(perm[L:R+1])
            if max_val == perm[X]:
                return False
        return True
    
    # Backtracking with early pruning
    def can_continue(perm, used):
        # Check constraints that can be fully evaluated
        for L, R, X in constraints:
            if R < len(perm):  # Range is completely filled
                max_val = max(perm[L:R+1])
                if max_val == perm[X]:
                    return False
        return True
    
    count = 0
    
    def backtrack(perm, used):
        nonlocal count
        
        if len(perm) == N:
            if is_valid(perm):
                count += 1
            return
        
        if not can_continue(perm, used):
            return
        
        for num in range(1, N + 1):
            if not used[num]:
                perm.append(num)
                used[num] = True
                backtrack(perm, used)
                perm.pop()
                used[num] = False
    
    used = [False] * (N + 1)
    backtrack([], used)
    
    print(count % MOD)

solve()
