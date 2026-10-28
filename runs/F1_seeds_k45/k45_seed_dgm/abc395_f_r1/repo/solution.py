def solve():
    N, X = map(int, input().split())
    teeth = []
    for _ in range(N):
        u, d = map(int, input().split())
        teeth.append((u, d))
    
    # Collect candidate H values
    # H = U_i + D_i for each tooth (these are the natural candidates)
    possible_H = set()
    for u, d in teeth:
        possible_H.add(u + d)
    
    min_cost = float('inf')
    
    for H in possible_H:
        # Try to make teeth fit with this H value using DP
        # For each tooth i, we need:
        # 1. u_i + d_i = H, so u_i = H - d_i
        # 2. u_i <= U_i (can only reduce)
        # 3. u_i >= 1 (teeth must be positive)
        # 4. |u_i - u_{i+1}| <= X (adjacent constraint)
        
        # Since u_i is determined by H and d_i, we can't freely choose u_i
        # But wait - we need exactly H - d_i, not the current d_i!
        # We're reducing both upper and lower teeth
        
        # Let me reconsider: if we reduce upper tooth to u_i and lower to d'_i
        # Then u_i + d'_i = H
        # Cost is (U_i - u_i) + (D_i - d'_i) = (U_i - u_i) + (D_i - (H - u_i)) = U_i + D_i - H
        
        # Oh! The cost for tooth i is constant: U_i + D_i - H
        # We just need to check if a valid sequence of u_i exists!
        
        # For tooth i: u_i = H - d'_i where d'_i >= 1
        # So u_i <= H - 1
        # Also u_i <= U_i and u_i >= 1
        
        # So valid range for u_i is: [max(1, H - D_i), min(U_i, H - 1)]
        
        valid = True
        for i in range(N):
            u, d = teeth[i]
            min_u = max(1, H - d)
            max_u = min(u, H - 1)
            
            if min_u > max_u:
                valid = False
                break
        
        if not valid:
            continue
        
        # Check if there's a valid sequence satisfying adjacency constraint
        # Use DP: dp[i][u] = whether we can reach position i with u_i = u
        
        # But u can be up to 10^9, so we need to track only relevant values
        # Relevant values: the min and max for each position
        
        def can_fit_with_constraint(H):
            # Check if we can find valid u_i sequence for this H
            # Using DP with range compression
            
            ranges = []
            for i in range(N):
                u, d = teeth[i]
                min_u = max(1, H - d)
                max_u = min(u, H - 1)
                
                if min_u > max_u:
                    return False
                ranges.append((min_u, max_u))
            
            # DP: for each position, track if it's reachable
            # Since ranges can be large, use interval DP
            
            # Can we reach position 0 with some u_0 in ranges[0]?
            curr_reachable = True  # Yes, any value in ranges[0]
            curr_range = ranges[0]
            
            for i in range(1, N):
                # From curr_range, what next_range is reachable?
                min_curr, max_curr = curr_range
                min_next, max_next = ranges[i]
                
                # We need to find intersection of reachable values with next range
                # Value next_u is reachable if exists curr_u in curr_range with |next_u - curr_u| <= X
                # This is true if next_u is within [min_curr - X, max_curr + X]
                
                # New reachable range is intersection of [min_curr - X, max_curr + X] and [min_next, max_next]
                new_min = max(min_next, min_curr - X)
                new_max = min(max_next, max_curr + X)
                
                if new_min > new_max:
                    return False
                
                curr_range = (new_min, new_max)
            
            return True
        
        if can_fit_with_constraint(H):
            # Cost is sum of U_i + D_i - H
            cost = sum(u + d - H for u, d in teeth)
            if cost >= 0:
                min_cost = min(min_cost, cost)
    
    print(min_cost if min_cost != float('inf') else 0)

solve()
