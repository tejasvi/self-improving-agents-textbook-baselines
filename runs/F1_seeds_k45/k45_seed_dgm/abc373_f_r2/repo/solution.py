import sys
from collections import defaultdict

def solve():
    N, W = map(int, input().split())
    items = []
    for _ in range(N):
        w, v = map(int, input().split())
        items.append((w, v))
    
    # For each item type, generate all beneficial items
    # The happiness for taking k items of type i is: k*v_i - k^2
    # The marginal gain for the k-th item is: v_i - (2k-1)
    # We should only take items with positive marginal gain
    
    all_items = []  # List of (weight, happiness_gain) for each item we can consider
    
    for w, v in items:
        k = 1
        while True:
            # Marginal happiness of taking the k-th item of this type
            marginal = v - (2*k - 1)
            if marginal <= 0:
                break
            # Weight would be k*w, marginal happiness gain is marginal
            # But we need to think in terms of individual items
            # When we take the k-th item, weight increases by w and happiness increases by marginal
            all_items.append((w, marginal))
            k += 1
            # Safety check: don't generate too many items
            if k * w > W:
                break
    
    # Now apply 0/1 knapsack DP with these items
    # dp[weight] = maximum happiness achievable with that weight
    dp = [0] * (W + 1)
    
    for w, happiness in all_items:
        # Process in reverse to avoid using same item multiple times
        for capacity in range(W, w - 1, -1):
            dp[capacity] = max(dp[capacity], dp[capacity - w] + happiness)
    
    print(dp[W])

solve()
