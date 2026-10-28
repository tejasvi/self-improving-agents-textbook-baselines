from typing import List
from math import gcd

class Solution:
    def subsequencePairCount(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        max_num = max(nums)
        
        result = 0
        
        # For each possible GCD value g:
        for g in range(1, max_num + 1):
            # Get elements divisible by g
            divisible = [num // g for num in nums if num % g == 0]
            if len(divisible) < 2:
                continue
            
            # Count pairs of disjoint subsequences with GCD = 1
            # among divisible elements (which means GCD = g for original elements)
            
            # DP: dp_pair[g1][g2] = ways to assign elements processed so far
            # where seq1 has GCD g1, seq2 has GCD g2
            # (g1=0 and g2=0 meaning both empty)
            
            dp_pair = {}
            dp_pair[(0, 0)] = 1  # both empty initially
            
            for elem in divisible:
                new_dp_pair = {}
                for (g1, g2), cnt in dp_pair.items():
                    # Case 1: element not used
                    key = (g1, g2)
                    new_dp_pair[key] = (new_dp_pair.get(key, 0) + cnt) % MOD
                    
                    # Case 2: element goes to seq1
                    new_g1 = gcd(g1, elem) if g1 > 0 else elem
                    key = (new_g1, g2)
                    new_dp_pair[key] = (new_dp_pair.get(key, 0) + cnt) % MOD
                    
                    # Case 3: element goes to seq2
                    new_g2 = gcd(g2, elem) if g2 > 0 else elem
                    key = (g1, new_g2)
                    new_dp_pair[key] = (new_dp_pair.get(key, 0) + cnt) % MOD
                
                dp_pair = new_dp_pair
            
            # Count pairs where g1 == g2 == 1 and both non-empty
            if (1, 1) in dp_pair:
                result = (result + dp_pair[(1, 1)]) % MOD
        
        return result
