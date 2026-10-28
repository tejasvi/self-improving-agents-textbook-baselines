#!/usr/bin/env python3

def solve():
    N, W = map(int, input().split())
    items = []
    for _ in range(N):
        w, v = map(int, input().split())
        items.append((w, v))
    
    # dp[weight] = maximum happiness achievable with weight at most weight
    dp = [0] * (W + 1)
    
    # For each item type
    for i in range(N):
        w_i, v_i = items[i]
        new_dp = dp.copy()
        
        # Try adding 1, 2, 3, ... items of type i
        # Maximum useful items is limited by:
        # 1. Weight constraint: k * w_i <= W
        # 2. Happiness is non-positive after k > v_i (since k*v_i - k^2 <= 0 for k >= v_i)
        # So we use min of both
        max_items = min(W // w_i, v_i)
        
        for k in range(1, max_items + 1):
            weight_used = k * w_i
            happiness_gained = k * v_i - k * k
            
            if weight_used > W:
                break
            
            # Update dp: for each previous weight, try adding k items of type i
            for prev_weight in range(W - weight_used + 1):
                new_weight = prev_weight + weight_used
                new_dp[new_weight] = max(new_dp[new_weight], dp[prev_weight] + happiness_gained)
        
        dp = new_dp
    
    print(max(dp))

solve()
