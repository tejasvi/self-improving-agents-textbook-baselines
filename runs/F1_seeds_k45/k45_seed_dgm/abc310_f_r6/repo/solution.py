# Write your solution here. Read from stdin, write to stdout.

MOD = 998244353

def modinv(a, m=MOD):
    """Compute modular inverse using Fermat's little theorem"""
    return pow(a, m - 2, m)

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    # Total number of outcomes
    total = 1
    for ai in a:
        total = (total * ai) % MOD
    
    # We need to count outcomes where at least one subset sums to 10
    # We use DP where:
    # dp[mask] = count of outcome sequences seen so far where mask represents
    #            which sums from 0 to 10 are achievable as subset sums
    # mask bit i = 1 iff sum i is achievable
    
    # Initially (no dice yet), only sum 0 is achievable (empty subset)
    dp = {}
    dp[1] = 1  # bit 0 set = sum 0 achievable
    
    for i in range(n):
        new_dp = {}
        
        # For each die i, it can show values 1 to a[i]
        # We need to accumulate results efficiently
        # Group by the transition they cause
        
        # For a given die with possible values 1 to max_v:
        # We need to process each value and update dp
        
        for v in range(1, a[i] + 1):
            # For each value v that die i can show:
            for mask, count in dp.items():
                # Compute new mask when die i shows value v
                new_mask = mask  # carry forward previous sums (by not including die i)
                
                # New sums from including die i (which shows v):
                # From each achievable sum s, we can get s + v
                for s in range(11):
                    if mask & (1 << s):  # if sum s is achievable
                        new_s = s + v
                        if new_s <= 10:
                            new_mask |= (1 << new_s)
                
                # Also value v by itself forms sum v
                if v <= 10:
                    new_mask |= (1 << v)
                
                # Only keep bits 0-10
                new_mask &= (1 << 11) - 1
                
                if new_mask not in new_dp:
                    new_dp[new_mask] = 0
                new_dp[new_mask] = (new_dp[new_mask] + count) % MOD
        
        dp = new_dp
    
    # Count outcomes where bit 10 (sum=10) is set
    answer = 0
    for mask, count in dp.items():
        if mask & (1 << 10):  # if sum 10 is achievable
            answer = (answer + count) % MOD
    
    # Convert to probability modulo MOD
    # answer / total modulo MOD
    # = answer * modinv(total) modulo MOD
    
    result = (answer * modinv(total)) % MOD
    print(result)

solve()
