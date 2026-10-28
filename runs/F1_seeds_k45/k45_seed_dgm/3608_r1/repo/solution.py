from typing import List
from math import gcd
from collections import defaultdict

class Solution:
    def subsequencePairCount(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        
        # dp[gcd1][gcd2] = number of ways to form subsequences with these GCDs
        # where 0 means the subsequence is empty
        dp = defaultdict(lambda: defaultdict(int))
        dp[0][0] = 1  # Initially, both subsequences are empty
        
        for num in nums:
            # Create a new dp for this iteration
            new_dp = defaultdict(lambda: defaultdict(int))
            
            # Copy all existing states (skip this number)
            for gcd1 in dp:
                for gcd2 in dp[gcd1]:
                    new_dp[gcd1][gcd2] = (new_dp[gcd1][gcd2] + dp[gcd1][gcd2]) % MOD
            
            # Try adding num to seq1 or seq2
            for gcd1 in dp:
                for gcd2 in dp[gcd1]:
                    count = dp[gcd1][gcd2]
                    
                    # Add num to seq1
                    new_gcd1 = gcd(gcd1, num) if gcd1 != 0 else num
                    new_dp[new_gcd1][gcd2] = (new_dp[new_gcd1][gcd2] + count) % MOD
                    
                    # Add num to seq2
                    new_gcd2 = gcd(gcd2, num) if gcd2 != 0 else num
                    new_dp[gcd1][new_gcd2] = (new_dp[gcd1][new_gcd2] + count) % MOD
            
            dp = new_dp
        
        # Count pairs where both GCDs are equal and non-zero
        result = 0
        for gcd_val in dp:
            if gcd_val > 0:  # Both must be non-empty
                result = (result + dp[gcd_val][gcd_val]) % MOD
        
        return result
