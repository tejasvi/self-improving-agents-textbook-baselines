from math import gcd
from typing import List

class Solution:
    def subsequencePairCount(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        
        # Use DP to track all possible states:
        # state[i][(g1, g2)] = number of ways to assign first i elements
        #                      such that seq1 has GCD g1, seq2 has GCD g2
        # where g1, g2 = 0 means the sequence is empty
        
        state = [dict() for _ in range(n + 1)]
        state[0][(0, 0)] = 1  # Initially both sequences are empty
        
        for i in range(n):
            for (g1, g2), count in state[i].items():
                # Option 1: Add nums[i] to seq1
                new_g1 = gcd(g1, nums[i]) if g1 != 0 else nums[i]
                key = (new_g1, g2)
                state[i + 1][key] = (state[i + 1].get(key, 0) + count) % MOD
                
                # Option 2: Add nums[i] to seq2
                new_g2 = gcd(g2, nums[i]) if g2 != 0 else nums[i]
                key = (g1, new_g2)
                state[i + 1][key] = (state[i + 1].get(key, 0) + count) % MOD
                
                # Option 3: Don't add nums[i] to either
                key = (g1, g2)
                state[i + 1][key] = (state[i + 1].get(key, 0) + count) % MOD
        
        # Count pairs where g1 = g2, g1 > 0 (both non-empty and equal GCD)
        result = 0
        for (g1, g2), count in state[n].items():
            if g1 == g2 and g1 > 0:
                result = (result + count) % MOD
        
        return result
