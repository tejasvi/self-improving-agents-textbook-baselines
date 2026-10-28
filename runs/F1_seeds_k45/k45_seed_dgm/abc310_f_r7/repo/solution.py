MOD = 998244353

def modinv(a, m=MOD):
    """Compute modular multiplicative inverse"""
    return pow(a, m - 2, m)

def solve():
    N = int(input())
    A = list(map(int, input().split()))
    
    # dp[reachable_sums] = count of outcomes
    # reachable_sums is a frozenset of integers from 1-10 that can be achieved
    
    from collections import defaultdict
    
    dp = defaultdict(int)
    dp[frozenset()] = 1  # Initially, no reachable sums, 1 way
    
    for die_idx in range(N):
        die_max = A[die_idx]
        new_dp = defaultdict(int)
        
        for reachable_sums, count in dp.items():
            # For each possible value this die shows (1 to die_max)
            for die_value in range(1, die_max + 1):
                # Build new set of reachable sums
                new_sums = set(reachable_sums)
                
                # We can choose to include this die or not
                # Case 1: Don't include this die
                new_dp[frozenset(new_sums)] = (new_dp[frozenset(new_sums)] + count) % MOD
                
                # Case 2: Include this die
                if die_value <= 10:
                    new_sums.add(die_value)
                for s in reachable_sums:
                    if s + die_value <= 10:
                        new_sums.add(s + die_value)
                new_dp[frozenset(new_sums)] = (new_dp[frozenset(new_sums)] + count) % MOD
        
        dp = new_dp
    
    # Count outcomes where 10 is in reachable sums
    favorable = 0
    for reachable_sums, count in dp.items():
        if 10 in reachable_sums:
            favorable = (favorable + count) % MOD
    
    # Total outcomes
    total = 1
    for a in A:
        total = (total * a) % MOD
    
    # Result = favorable / total (mod MOD)
    result = (favorable * modinv(total)) % MOD
    print(result)

solve()
