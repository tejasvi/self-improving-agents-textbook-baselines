# Write your solution here. Read from stdin, write to stdout.

MOD = 998244353

def modinv(a, m=MOD):
    """Compute modular inverse using Fermat's little theorem"""
    return pow(a, m - 2, m)

def solve():
    N = int(input())
    A = list(map(int, input().split()))
    
    # Total number of outcomes
    total = 1
    for a in A:
        total = (total * a) % MOD
    
    # DP approach: for each die, track which sums 0-10 are achievable
    # We use a bitmask where bit i is set if sum i is achievable
    # mask = 1 << i means sum i is achievable
    
    # dp[mask] = count of outcomes (of first i dice) that achieve sums given by mask
    
    # Initialize: with 0 dice, only sum 0 is achievable (empty subset)
    dp = {1: 1}  # mask = 1 means only bit 0 is set, representing sum 0
    
    for i in range(N):
        new_dp = {}
        
        # For each current state
        for mask, count in dp.items():
            # For each possible value of die i
            for die_value in range(1, A[i] + 1):
                # Compute new achievable sums
                new_mask = mask  # We always have the sums from not including die i
                
                # If we include die i, we can form new sums
                for s in range(11):
                    if (mask >> s) & 1:  # If sum s was achievable
                        new_sum = s + die_value
                        if new_sum <= 10:
                            new_mask |= (1 << new_sum)
                
                # Also die_value by itself (but this is covered by 0 + die_value)
                
                if new_mask not in new_dp:
                    new_dp[new_mask] = 0
                new_dp[new_mask] = (new_dp[new_mask] + count) % MOD
        
        dp = new_dp
    
    # Count outcomes where sum 10 is achievable
    favorable = 0
    for mask, count in dp.items():
        if (mask >> 10) & 1:  # If bit 10 is set
            favorable = (favorable + count) % MOD
    
    # Compute probability = favorable / total
    result = (favorable * modinv(total)) % MOD
    print(result)

solve()
