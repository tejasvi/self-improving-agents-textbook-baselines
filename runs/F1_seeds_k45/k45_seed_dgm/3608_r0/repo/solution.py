from typing import List
from math import gcd

class Solution:
    def subsequencePairCount(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        
        # dp[i] = dictionary mapping (g1, g2) -> count
        # where g1 is GCD of seq1, g2 is GCD of seq2 after processing first i elements
        # g1=0 means seq1 is empty, g2=0 means seq2 is empty
        
        dp = [dict() for _ in range(n + 1)]
        dp[0][(0, 0)] = 1
        
        for i in range(n):
            elem = nums[i]
            for (g1, g2), cnt in dp[i].items():
                # Choice 1: Add element to seq1
                new_g1 = gcd(g1, elem) if g1 != 0 else elem
                key = (new_g1, g2)
                dp[i + 1][key] = (dp[i + 1].get(key, 0) + cnt) % MOD
                
                # Choice 2: Add element to seq2
                new_g2 = gcd(g2, elem) if g2 != 0 else elem
                key = (g1, new_g2)
                dp[i + 1][key] = (dp[i + 1].get(key, 0) + cnt) % MOD
                
                # Choice 3: Don't add element
                key = (g1, g2)
                dp[i + 1][key] = (dp[i + 1].get(key, 0) + cnt) % MOD
        
        # Count pairs where g1 == g2 and both are non-zero
        result = 0
        for (g1, g2), cnt in dp[n].items():
            if g1 == g2 and g1 != 0:
                result = (result + cnt) % MOD
        
        return result
