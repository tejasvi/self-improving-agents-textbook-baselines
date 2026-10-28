MOD = 998244353

def solve():
    N, M = map(int, input().split())
    conditions = []
    for _ in range(M):
        L, R, X = map(int, input().split())
        conditions.append((L-1, R-1, X-1))  # Convert to 0-indexed
    
    def check_conditions(perm):
        for L, R, X in conditions:
            # Find max in range [L, R]
            max_val = max(perm[L:R+1])
            # Check if P_X is NOT the max
            if perm[X] == max_val:
                return False
        return True
    
    # Generate all permutations and count valid ones
    from itertools import permutations
    
    count = 0
    for perm in permutations(range(1, N+1)):
        if check_conditions(perm):
            count += 1
    
    print(count % MOD)

solve()
