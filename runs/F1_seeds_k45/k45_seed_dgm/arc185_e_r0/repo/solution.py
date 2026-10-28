from math import gcd
from collections import defaultdict

MOD = 998244353

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    # Dictionary: last_element_value -> [count, score_sum]
    dp = defaultdict(lambda: [0, 0])
    
    # For each m from 1 to n
    for m in range(n):
        new_dp = defaultdict(lambda: [0, 0])
        
        # Option 1: Start a new subsequence with just a[m]
        new_dp[a[m]][0] += 1
        
        # Option 2: Extend existing subsequences with a[m]
        for last_val in dp:
            count, score_sum = dp[last_val]
            # Extend the subsequence
            gcd_val = gcd(last_val, a[m])
            new_dp[a[m]][0] += count
            new_dp[a[m]][1] += score_sum + count * gcd_val
        
        # Merge old dp with new_dp (keep all subsequences from before)
        for val in dp:
            new_dp[val][0] += dp[val][0]
            new_dp[val][1] += dp[val][1]
        
        dp = new_dp
        
        # Sum all scores
        total_score = 0
        for val in dp:
            total_score += dp[val][1]
        
        print(total_score % MOD)

solve()
