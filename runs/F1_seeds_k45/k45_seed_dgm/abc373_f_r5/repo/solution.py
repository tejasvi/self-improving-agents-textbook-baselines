# Write your solution here. Read from stdin, write to stdout.

def solve():
    N, W = map(int, input().split())
    items = []
    for _ in range(N):
        w, v = map(int, input().split())
        items.append((w, v))
    
    # dp[w] = maximum happiness with weight at most w
    dp = [0] * (W + 1)
    
    # For each item type
    for w, v in items:
        # For this item type, we'll consider taking different numbers of items
        # The happiness from k items is: k*v - k^2
        # We need to find the maximum number of items worth taking
        # The marginal value of the k-th item is: v - 2*k
        # We should stop when marginal value becomes negative or weight is exceeded
        
        # Maximum items we could possibly take
        max_items = W // w + 1
        
        # Create a new DP array for this item type
        # We'll iterate through possible counts and update DP carefully
        new_dp = dp.copy()
        
        for k in range(1, max_items):
            total_weight = k * w
            if total_weight > W:
                break
            
            happiness = k * v - k * k
            
            # Update DP: for each weight, consider adding k items of current type
            for prev_w in range(W - total_weight, -1, -1):
                new_dp[prev_w + total_weight] = max(new_dp[prev_w + total_weight], 
                                                      dp[prev_w] + happiness)
        
        dp = new_dp
    
    print(max(dp))

solve()
