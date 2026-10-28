def solve():
    N, W = map(int, input().split())
    items = []
    for _ in range(N):
        w, v = map(int, input().split())
        items.append((w, v))
    
    # dp[weight] = maximum happiness achievable with exactly weight capacity used
    # We'll use dp[weight] for weight from 0 to W
    dp = [0] * (W + 1)
    
    # For each item type
    for w_i, v_i in items:
        # We need to process this in reverse to handle unlimited items correctly
        # But we limit the number of items we consider for this type
        # Since happiness = k*v_i - k^2, the maximum useful k is around v_i/2
        # But we also need to consider weight constraint: k*w_i <= W
        max_k = min(v_i, W // w_i) + 1  # +1 for safety margin
        
        # Create a new dp array for this item type
        new_dp = dp.copy()
        
        # For each possible quantity of this item type
        for k in range(1, max_k + 1):
            happiness = k * v_i - k * k
            weight_needed = k * w_i
            
            if weight_needed > W:
                break
            
            # Update dp: for each previous weight, try adding k items of type i
            for prev_weight in range(W - weight_needed + 1):
                new_dp[prev_weight + weight_needed] = max(
                    new_dp[prev_weight + weight_needed],
                    dp[prev_weight] + happiness
                )
        
        dp = new_dp
    
    # The answer is the maximum value in dp
    return max(dp)

print(solve())
