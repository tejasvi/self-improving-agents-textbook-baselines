from typing import List
from math import gcd
from functools import reduce

class Solution:
    def subsequencePairCount(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        
        # dp[mask] = dictionary mapping GCD value to count of subsequences with that GCD
        # using elements from indices in mask
        dp = {}
        
        # Initialize: for each single element, it forms a subsequence with GCD = itself
        for i in range(n):
            mask = 1 << i
            dp[mask] = {nums[i]: 1}
        
        # Build all possible subsequences
        for mask in range(1, 1 << n):
            if mask not in dp:
                dp[mask] = {}
            
            # Try to extend by combining smaller masks
            # Find all ways to build this mask from submasks
            submask = mask
            while submask > 0:
                complement = mask ^ submask
                if complement > 0 and submask > 0 and complement in dp and submask in dp:
                    # Combine subsequences with GCDs from submask and complement
                    for gcd1, cnt1 in dp[submask].items():
                        for gcd2, cnt2 in dp[complement].items():
                            combined_gcd = gcd(gcd1, gcd2)
                            if combined_gcd not in dp[mask]:
                                dp[mask][combined_gcd] = 0
                            dp[mask][combined_gcd] = (dp[mask][combined_gcd] + cnt1 * cnt2) % MOD
                
                submask = (submask - 1) & mask
        
        # Count pairs of disjoint subsequences with equal GCD
        result = 0
        
        # Iterate through all pairs of disjoint masks
        for mask1 in range(1, 1 << n):
            for mask2 in range(1, 1 << n):
                # Check if they are disjoint
                if mask1 & mask2 == 0:
                    # Count pairs with equal GCD
                    if mask1 in dp and mask2 in dp:
                        for g in dp[mask1]:
                            if g in dp[mask2]:
                                result = (result + dp[mask1][g] * dp[mask2][g]) % MOD
        
        return result
