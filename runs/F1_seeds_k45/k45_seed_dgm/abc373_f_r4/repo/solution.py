# Write your solution here. Read from stdin, write to stdout.

def solve():
    N, W = map(int, input().split())
    items = []
    for _ in range(N):
        w, v = map(int, input().split())
        items.append((w, v))
    
    # dp[weight] = maximum happiness achievable with this weight
    dp = [0] * (W + 1)
    
    # Process each item type
    for w_i, v_i in items:
        # The happiness function is k*v_i - k^2
        # It's maximized at k = v_i/2
        # For k > v_i, the happiness becomes negative
        # So we only need to consider k up to v_i
        max_k = W // w_i  # Maximum k based on weight constraint
        max_k = min(max_k, v_i)  # But not more than v_i
        
        # Create a new dp array for this item type
        new_dp = dp[:]
        
        # For each current weight state
        for current_weight in range(W + 1):
            # Try adding k items of type i to this state
            for k in range(1, max_k + 1):
                if current_weight + k * w_i > W:
                    break
                new_weight = current_weight + k * w_i
                happiness_added = k * v_i - k * k
                new_value = dp[current_weight] + happiness_added
                new_dp[new_weight] = max(new_dp[new_weight], new_value)
        
        dp = new_dp
    
    print(max(dp))

solve()
