from typing import List
from math import gcd
from functools import reduce

class Solution:
    def subsequencePairCount(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        
        # dp[i] = dictionary where dp[i][(g1, g2)] = count of ways to form subsequences 
        # with gcd g1 and g2 using first i elements
        # We only track states where at least one subsequence is non-empty
        
        # Start with empty state: no subsequences formed yet
        dp = [{} for _ in range(len(nums) + 1)]
        dp[0][(0, 0)] = 1  # (g1=0, g2=0) means no elements in either subsequence
        
        for i in range(len(nums)):
            # Copy previous states (don't use nums[i])
            for key, count in dp[i].items():
                if key not in dp[i + 1]:
                    dp[i + 1][key] = 0
                dp[i + 1][key] = (dp[i + 1][key] + count) % MOD
            
            # Add nums[i] to seq1
            for (g1, g2), count in dp[i].items():
                new_g1 = gcd(g1, nums[i]) if g1 != 0 else nums[i]
                key = (new_g1, g2)
                if key not in dp[i + 1]:
                    dp[i + 1][key] = 0
                dp[i + 1][key] = (dp[i + 1][key] + count) % MOD
            
            # Add nums[i] to seq2
            for (g1, g2), count in dp[i].items():
                new_g2 = gcd(g2, nums[i]) if g2 != 0 else nums[i]
                key = (g1, new_g2)
                if key not in dp[i + 1]:
                    dp[i + 1][key] = 0
                dp[i + 1][key] = (dp[i + 1][key] + count) % MOD
        
        # Count pairs where both subsequences are non-empty and have equal GCD
        result = 0
        for (g1, g2), count in dp[len(nums)].items():
            if g1 != 0 and g2 != 0 and g1 == g2:
                result = (result + count) % MOD
        
        return result
