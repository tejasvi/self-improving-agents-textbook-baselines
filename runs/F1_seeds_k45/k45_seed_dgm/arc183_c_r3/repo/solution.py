MOD = 998244353

def read_input():
    N, M = map(int, input().split())
    conditions = []
    for _ in range(M):
        L, R, X = map(int, input().split())
        conditions.append((L-1, R-1, X-1))  # Convert to 0-indexed
    return N, M, conditions

def check_final_permutation(perm, conditions):
    """Check if a complete permutation satisfies all conditions."""
    for L, R, X in conditions:
        max_val = max(perm[L:R+1])
        if max_val == perm[X]:
            return False
    return True

def can_prune(perm, num_assigned, conditions, N):
    """
    Check if current partial permutation can violate any constraint.
    Returns False if definitely violates a constraint, True otherwise.
    """
    # Get set of assigned values
    assigned_values = set(perm[:num_assigned])
    available_values = set(range(1, N+1)) - assigned_values
    
    for L, R, X in conditions:
        # Get assigned positions in range [L, R]
        assigned_in_range = []
        for i in range(L, R+1):
            if i < num_assigned:
                assigned_in_range.append(i)
        
        if not assigned_in_range:
            # No positions assigned in this range yet
            continue
        
        max_in_range = max(perm[i] for i in assigned_in_range)
        
        # Check if all positions in range are assigned
        all_in_range_assigned = all(i < num_assigned for i in range(L, R+1))
        
        if all_in_range_assigned:
            # All positions in range are assigned
            if X < num_assigned:
                # X is also assigned
                if perm[X] == max_in_range:
                    return False  # Constraint violated
        else:
            # Some positions in range are not yet assigned
            if X < num_assigned:
                # X is assigned but range is not complete
                if perm[X] == max_in_range:
                    # Need to place a value > max_in_range in the remaining positions
                    if not any(v > max_in_range for v in available_values):
                        return False  # Can't satisfy this constraint
    
    return True

def backtrack(perm, num_assigned, N, conditions):
    """
    Build permutation position by position.
    perm: array where perm[0..num_assigned-1] are assigned
    num_assigned: number of positions assigned
    """
    if num_assigned == N:
        # All positions assigned, check if valid
        return 1 if check_final_permutation(perm, conditions) else 0
    
    count = 0
    used_values = set(perm[:num_assigned])
    
    # Try each value that hasn't been used
    for val in range(1, N+1):
        if val not in used_values:
            perm[num_assigned] = val
            
            # Check if we can prune
            if can_prune(perm, num_assigned+1, conditions, N):
                count += backtrack(perm, num_assigned+1, N, conditions)
    
    return count

def solve(N, M, conditions):
    """Count valid permutations"""
    perm = [0] * N
    return backtrack(perm, 0, N, conditions)

def main():
    N, M, conditions = read_input()
    result = solve(N, M, conditions)
    print(result % MOD)

if __name__ == "__main__":
    main()
