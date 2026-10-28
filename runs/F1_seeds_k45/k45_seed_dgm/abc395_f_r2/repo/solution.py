def solve():
    N, X = map(int, input().split())
    teeth = []
    for _ in range(N):
        u, d = map(int, input().split())
        teeth.append((u, d))
    
    # Total cost = sum(U_i + D_i) - N*H
    # We want to maximize H to minimize cost
    
    total_sum = sum(u + d for u, d in teeth)
    
    # H can be at most min(U_i + D_i) for all i
    max_H = min(u + d for u, d in teeth)
    
    def can_achieve_H(H):
        """Check if we can achieve constant sum H with valid upper teeth sequence"""
        # For position i, upper tooth length U'_i must satisfy:
        # - max(0, H - D_i) ≤ U'_i ≤ U_i (from constraints)
        # - |U'_i - U'_{i+1}| ≤ X (smoothness constraint)
        
        # Track valid range at each position
        min_u, max_u = teeth[0][0], teeth[0][0]
        min_val = max(0, H - teeth[0][1])
        max_val = teeth[0][0]
        
        if min_val > max_val:
            return False
        
        current_min = min_val
        current_max = max_val
        
        for i in range(1, N):
            # Constraints at position i
            min_ui = max(0, H - teeth[i][1])
            max_ui = teeth[i][0]
            
            if min_ui > max_ui:
                return False
            
            # After moving from previous position with constraint |U_i - U_{i+1}| ≤ X
            # Previous position could be in [current_min, current_max]
            # Current position can be in [current_min - X, current_max + X]
            
            new_min = max(min_ui, current_min - X)
            new_max = min(max_ui, current_max + X)
            
            if new_min > new_max:
                return False
            
            current_min = new_min
            current_max = new_max
        
        return True
    
    # Binary search for maximum valid H
    left, right = 1, max_H
    best_H = 0
    
    while left <= right:
        mid = (left + right) // 2
        if can_achieve_H(mid):
            best_H = mid
            left = mid + 1
        else:
            right = mid - 1
    
    # Calculate and print cost
    cost = total_sum - N * best_H
    print(cost)

solve()
