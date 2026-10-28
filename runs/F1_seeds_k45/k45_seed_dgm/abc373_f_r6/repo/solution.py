def solve():
    N, W = map(int, input().split())
    items = []
    for _ in range(N):
        w, v = map(int, input().split())
        items.append((w, v))
    
    # dp[weight] = maximum happiness with exactly this weight
    dp = [float('-inf')] * (W + 1)
    dp[0] = 0
    
    # For each item type
    for w, v in items:
        # Calculate how many items of this type we should consider
        # Marginal value of k-th item is v - 2(k-1)
        # We only consider items with positive marginal value
        # v - 2(k-1) > 0 => k < v/2 + 1
        # But also bounded by W // w (can't fit more than this many items)
        max_count = min(v // 2 + 1, W // w)
        
        # Create a new dp table for this item type
        new_dp = [float('-inf')] * (W + 1)
        
        # For each current weight
        for current_weight in range(W + 1):
            if dp[current_weight] == float('-inf'):
                continue
            
            # Try taking k items of this type
            for k in range(max_count + 1):
                total_weight = current_weight + k * w
                if total_weight > W:
                    break
                
                if k == 0:
                    happiness = 0
                else:
                    happiness = k * v - k * k
                
                new_dp[total_weight] = max(new_dp[total_weight], dp[current_weight] + happiness)
        
        dp = new_dp
    
    return max(dp)

print(solve())
