#!/usr/bin/env python3

def solve():
    N, W = map(int, input().split())
    items = []
    for _ in range(N):
        w, v = map(int, input().split())
        items.append((w, v))
    
    # dp[w] = maximum happiness using at most weight w
    dp = [0] * (W + 1)
    
    # Process each item type separately (bounded knapsack)
    for w, v in items:
        # For this item type, determine maximum number of items to consider
        # We can't take more than W/w items due to weight constraint
        max_by_weight = W // w
        
        # The happiness function is k*v - k^2 >= 0 requires k*(v - k) >= 0
        # So k <= v (we don't want negative happiness)
        # We consider k from 1 to min(max_by_weight, v)
        max_items = min(max_by_weight, v)
        
        # Create a new dp array for this item type
        new_dp = dp[:]
        
        # Try all possible quantities of this item
        for k in range(1, max_items + 1):
            weight_needed = k * w
            if weight_needed > W:
                break
            
            happiness = k * v - k * k
            
            # Update new_dp: for each existing weight from dp, try adding k items
            for current_w in range(W, weight_needed - 1, -1):
                new_dp[current_w] = max(new_dp[current_w], 
                                        dp[current_w - weight_needed] + happiness)
        
        dp = new_dp
    
    print(max(dp))

solve()
