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
    # We'll use DP: dp[i][mask] = number of ways to achieve subset sum mask using first i dice
    # where mask represents which sums (0-10) are achievable
    
    # Instead, let's think of it differently:
    # For each outcome of dice, we need to check if a subset sum equals 10
    # We can use DP where we track all possible subset sums achievable
    
    # dp[i][s] = number of ways where using first i dice, 
    # we can achieve subset sum s (0 <= s <= 10) as an achievable sum
    
    # Actually, we need: for each die outcome, track which sums are achievable
    # Then count outcomes where 10 is achievable
    
    # Better approach: 
    # dp[i] = dictionary where key is a frozenset of achievable sums, 
    # value is count of ways to get that configuration
    
    from collections import defaultdict
    
    # dp[achievable_sums] = count
    # achievable_sums is represented as a tuple of which sums (0-10) are achievable
    dp = defaultdict(int)
    dp[tuple([True] + [False] * 10)] = 1  # Initially, sum 0 is achievable (empty subset)
    
    for die_idx in range(n):
        new_dp = defaultdict(int)
        
        # For each current state
        for sums_tuple, count in dp.items():
            sums = list(sums_tuple)  # sums[i] = True if sum i is achievable
            
            # For each possible outcome of this die (1 to a[die_idx])
            for outcome in range(1, a[die_idx] + 1):
                new_sums = sums[:]
                
                # If we add this outcome to any achievable sum, what new sums become achievable?
                # We need to check all currently achievable sums
                for s in range(11):
                    if sums[s] and s + outcome <= 10:
                        new_sums[s + outcome] = True
                
                # Also, the outcome itself as a single die is achievable
                if outcome <= 10:
                    new_sums[outcome] = True
                
                new_tuple = tuple(new_sums)
                new_dp[new_tuple] = (new_dp[new_tuple] + count) % MOD
        
        dp = new_dp
    
    # Count outcomes where sum 10 is achievable
    favorable = 0
    for sums_tuple, count in dp.items():
        if sums_tuple[10]:  # If sum 10 is achievable
            favorable = (favorable + count) % MOD
    
    # Compute probability = favorable / total (mod MOD)
    result = (favorable * modinv(total)) % MOD
    print(result)

solve()
