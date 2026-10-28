# Write your solution here. Read from stdin, write to stdout.

def solve():
    N, X = map(int, input().split())
    teeth = []
    for _ in range(N):
        u, d = map(int, input().split())
        teeth.append((u, d))
    
    # The minimum H must be at least max(U_i + D_i)
    min_H = max(u + d for u, d in teeth)
    
    def cost_for_H(H):
        """
        For a given H, find minimum cost using DP.
        
        For each tooth i, we need to choose u_i such that:
        - u_i + d_i = H (so d_i is determined)
        - u_i <= U_i (can only reduce upper teeth)
        - d_i <= D_i (can only reduce lower teeth), which means u_i >= H - D_i
        - |u_i - u_{i+1}| <= X (consecutive constraint)
        
        Cost = sum of reductions = sum(U_i - u_i) + sum(D_i - d_i)
                                 = sum(U_i - u_i) + sum(D_i - (H - u_i))
                                 = sum(U_i + D_i - H)
                                 = N*H - sum(U_i + D_i)
        
        Wait, that's not right. Let me recalculate.
        
        For pair i, if we set u_i and d_i = H - u_i:
        - Cost for upper tooth i: max(0, U_i - u_i)
        - Cost for lower tooth i: max(0, D_i - d_i) = max(0, D_i - (H - u_i))
        - Total cost for pair i: max(0, U_i - u_i) + max(0, D_i - H + u_i)
        
        If H >= U_i + D_i:
            - Cost = (U_i - u_i) + (D_i - H + u_i) = U_i + D_i - H (fixed)
        
        Actually if u_i <= U_i and H - u_i <= D_i:
            The cost is exactly U_i + D_i - H
        
        So total cost = sum(U_i + D_i) - N*H
        
        The problem is to find u_1, ..., u_N such that:
        - H - D_i <= u_i <= U_i for all i
        - |u_i - u_{i+1}| <= X for all i
        
        If we can satisfy these constraints, total cost is sum(U_i + D_i) - N*H
        So we want to maximize H!
        """
        
        # Check if H is feasible
        # For each tooth, determine valid range for u_i
        valid_ranges = []
        for u, d in teeth:
            min_u = max(0, H - d)  # Lower bound from lower tooth constraint
            max_u = min(u, H)       # Upper bound from upper tooth constraint
            if min_u > max_u:
                return None  # Impossible for this H
            valid_ranges.append((min_u, max_u))
        
        # Now check if we can find u_1, ..., u_N satisfying the adjacency constraint
        # This is a DP problem
        
        # dp[i][u] = True if we can make first i teeth fit with i-th upper tooth at u
        # But we need to discretize u values
        
        # Collect all important u values
        important_u = set()
        for min_u, max_u in valid_ranges:
            important_u.add(min_u)
            important_u.add(max_u)
        
        # Also add intermediate values
        for min_u, max_u in valid_ranges:
            # We should consider all integers in range, but that's too many
            # The DP transitions only care about values within X distance
            # So we can consider a subset
            if max_u - min_u <= 2 * X:
                for v in range(min_u, max_u + 1):
                    important_u.add(v)
            else:
                # Add boundary points and samples
                for v in range(min_u, min(min_u + X + 1, max_u + 1)):
                    important_u.add(v)
                for v in range(max(max_u - X, min_u), max_u + 1):
                    important_u.add(v)
        
        # DP
        dp = [set() for _ in range(N)]
        
        # Initialize first tooth
        min_u, max_u = valid_ranges[0]
        for u_val in important_u:
            if min_u <= u_val <= max_u:
                dp[0].add(u_val)
        
        # Fill DP
        for i in range(1, N):
            min_u_i, max_u_i = valid_ranges[i]
            
            for u_val in important_u:
                if min_u_i <= u_val <= max_u_i:
                    # Check if we can transition from some previous state
                    for prev_u in dp[i-1]:
                        if abs(u_val - prev_u) <= X:
                            dp[i].add(u_val)
                            break
        
        # Check if we found a solution
        if dp[N-1]:
            return sum(u + d for u, d in teeth) - N * H
        return None
    
    # Try increasing H until we find a feasible solution
    # Start from min_H
    for H in range(min_H, min_H + 10**9):  # Upper bound is generous
        cost = cost_for_H(H)
        if cost is not None:
            print(cost)
            return
    
    print(-1)  # Should not reach here

solve()
