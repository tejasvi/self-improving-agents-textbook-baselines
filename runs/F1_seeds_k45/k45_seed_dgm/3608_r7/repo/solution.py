from typing import List
from math import gcd
from functools import reduce

class Solution:
    def subsequencePairCount(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        
        # dp[gcd1][gcd2] = number of ways to form subsequences with GCD gcd1 and gcd2
        # gcd1=0 means seq1 is empty, gcd2=0 means seq2 is empty
        dp = {}
        
        for num in nums:
            new_dp = dp.copy()
            
            # Case 1: Add current num to seq1
            # (0, g) -> (num, g)
            if (0, 0) not in new_dp:
                new_dp[(0, 0)] = 0
            new_dp[(num, 0)] = new_dp.get((num, 0), 0) + new_dp.get((0, 0), 0)
            
            # (0, g) -> (num, g) where g != 0
            for (g1, g2), count in dp.items():
                if g1 == 0 and g2 != 0:
                    new_g1 = num
                    new_dp[(new_g1, g2)] = new_dp.get((new_g1, g2), 0) + count
            
            # (g, h) -> (gcd(g, num), h)
            for (g1, g2), count in dp.items():
                if g1 != 0 and g2 != 0:
                    new_g1 = gcd(g1, num)
                    new_dp[(new_g1, g2)] = new_dp.get((new_g1, g2), 0) + count
                elif g1 != 0 and g2 == 0:
                    new_g1 = gcd(g1, num)
                    new_dp[(new_g1, g2)] = new_dp.get((new_g1, g2), 0) + count
            
            # Case 2: Add current num to seq2
            # (g, 0) -> (g, num)
            if (0, 0) not in new_dp:
                new_dp[(0, 0)] = 0
            new_dp[(0, num)] = new_dp.get((0, num), 0) + new_dp.get((0, 0), 0)
            
            # (g, 0) -> (g, num) where g != 0
            for (g1, g2), count in dp.items():
                if g1 != 0 and g2 == 0:
                    new_g2 = num
                    new_dp[(g1, new_g2)] = new_dp.get((g1, new_g2), 0) + count
            
            # (g, h) -> (g, gcd(h, num))
            for (g1, g2), count in dp.items():
                if g1 != 0 and g2 != 0:
                    new_g2 = gcd(g2, num)
                    new_dp[(g1, new_g2)] = new_dp.get((g1, new_g2), 0) + count
                elif g1 == 0 and g2 != 0:
                    new_g2 = gcd(g2, num)
                    new_dp[(g1, new_g2)] = new_dp.get((g1, new_g2), 0) + count
            
            # Case 3: Don't add current num (already handled by copy)
            
            # Initialize for starting new subsequences
            if (0, 0) not in new_dp:
                new_dp[(0, 0)] = 1
            else:
                new_dp[(0, 0)] += 1
            
            dp = new_dp
        
        # Sum up all pairs where gcd1 == gcd2 and both are non-empty
        result = 0
        for (g1, g2), count in dp.items():
            if g1 == g2 and g1 != 0:
                result = (result + count) % MOD
        
        return result
