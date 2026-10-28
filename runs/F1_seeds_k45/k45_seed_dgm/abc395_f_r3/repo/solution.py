def can_achieve_H(U, D, X, H, N):
    """
    Check if we can achieve target sum H for all pairs (U_i', D_i') such that:
    - U_i' + D_i' = H for all i
    - 0 <= U_i' <= U_i and 0 <= D_i' <= D_i for all i
    - |U_i' - U_{i+1}'| <= X for consecutive upper teeth
    """
    # For each position i, U_i' must satisfy:
    # - U_i' <= U_i (can't increase)
    # - U_i' <= H (since D_i' = H - U_i' >= 0)
    # - U_i' >= H - D_i (since D_i' <= D_i)
    # - |U_i' - U_{i+1}'| <= X (consecutive constraint)
    
    # Calculate valid range for each position
    ranges = []
    for i in range(N):
        min_u = max(0, H - D[i])
        max_u = min(U[i], H)
        if min_u > max_u:
            return False
        ranges.append((min_u, max_u))
    
    # Use DP/greedy to check if valid sequence exists
    # For position 0, we can choose any value in its range
    # For position i, we need to choose a value that:
    # - is in its range
    # - differs by at most X from position i-1
    
    # We'll use a greedy/DP approach to check feasibility
    # Track the minimum and maximum possible values at each position
    
    min_val, max_val = ranges[0][0], ranges[0][1]
    
    for i in range(1, N):
        # Values at position i must be within [min_val - X, max_val + X]
        # and also within ranges[i]
        new_min = max(ranges[i][0], min_val - X)
        new_max = min(ranges[i][1], max_val + X)
        
        if new_min > new_max:
            return False
        
        min_val, max_val = new_min, new_max
    
    return True


def solve():
    N, X = map(int, input().split())
    U = []
    D = []
    for _ in range(N):
        u, d = map(int, input().split())
        U.append(u)
        D.append(d)
    
    # Binary search on H
    # H must be at least 1 (since we need positive values)
    # H can be at most sum of all U_i + D_i (worst case no reduction)
    
    left, right = 0, max(U[i] + D[i] for i in range(N))
    
    # Find maximum H
    best_H = 0
    while left <= right:
        mid = (left + right) // 2
        if can_achieve_H(U, D, X, mid, N):
            best_H = mid
            left = mid + 1
        else:
            right = mid - 1
    
    # Cost is sum of all U_i + D_i minus N * best_H
    total_sum = sum(U[i] + D[i] for i in range(N))
    cost = total_sum - N * best_H
    
    print(cost)


solve()
