from typing import List
from math import gcd
from functools import reduce

class Solution:
    def subsequencePairCount(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        max_num = max(nums)
        
        # For each possible GCD value, count subsequences with exactly that GCD
        # dp[g] = number of non-empty subsequences with GCD exactly equal to g
        dp = {}
        
        # First, count subsequences for each possible GCD
        # We'll use dynamic programming where we track (GCD -> count of subsequences with that GCD)
        
        # For each element, we decide to include it or not
        # gcd_count[g] = number of subsequences with GCD g
        gcd_count = {}
        
        for num in nums:
            new_gcd_count = gcd_count.copy()
            
            # Add num as a single element subsequence
            if num not in new_gcd_count:
                new_gcd_count[num] = 0
            new_gcd_count[num] += 1
            
            # Extend existing subsequences with num
            for g, count in gcd_count.items():
                new_g = gcd(g, num)
                if new_g not in new_gcd_count:
                    new_gcd_count[new_g] = 0
                new_gcd_count[new_g] += count
            
            gcd_count = new_gcd_count
        
        result = 0
        
        # For each possible GCD value
        for g in gcd_count:
            # We need to count pairs of disjoint subsequences both with GCD g
            # Filter elements that are divisible by g
            divisible = [x for x in nums if x % g == 0]
            m = len(divisible)
            
            # For divisible elements, count subsequences with GCD exactly g
            # dp2[i][h] = count of subsequences using first i elements with GCD h
            # But we only care about GCD g
            
            # Better approach: for elements divisible by g,
            # count subsequences with GCD exactly g
            # Then pairs of disjoint such subsequences
            
            # For each element divisible by g, we have 3 choices:
            # 1. Include in seq1
            # 2. Include in seq2
            # 3. Don't include
            
            # We need both seq1 and seq2 to:
            # - Be non-empty
            # - Have GCD exactly g
            
            # Count[g] = number of non-empty subsequences of divisible elements with GCD exactly g
            count_g = self._count_subsequences_with_gcd(divisible, g)
            
            # The number of ordered pairs (seq1, seq2) both with GCD g and disjoint
            # Each pair assignment: for each element, choose seq1, seq2, or neither
            # Total ways = 3^m
            # Ways with seq1 or seq2 empty: counted by (2^m - 1) for each
            # But we need inclusion-exclusion over all GCDs
            
            # Actually, let's think differently:
            # For each element divisible by g, assign to seq1, seq2, or neither
            # This gives 3^m total assignments
            # From this, subtract cases where seq1 is empty or seq2 is empty
            # But we also need to ensure GCD is exactly g
            
            # Let me use a DP approach instead
            # dp[i][g1][g2] = ways to assign first i elements to seq1/seq2/neither
            #                  such that seq1 has GCD g1 and seq2 has GCD g2
            
            result += self._count_disjoint_pairs(divisible, g)
            result %= MOD
        
        return result
    
    def _count_subsequences_with_gcd(self, nums, target_gcd):
        """Count non-empty subsequences of nums with GCD exactly equal to target_gcd"""
        if not nums:
            return 0
        
        MOD = 10**9 + 7
        
        # dp[g] = count of subsequences with GCD exactly g
        # We only care about target_gcd
        
        # First pass: count subsequences with GCD >= target_gcd (divisible by target_gcd)
        # Then use inclusion-exclusion
        
        # Let's use a different approach:
        # gcd_count[g] = subsequences with GCD exactly g
        gcd_count = {}
        
        for num in nums:
            new_gcd_count = gcd_count.copy()
            
            # Add num as single element
            if num not in new_gcd_count:
                new_gcd_count[num] = 0
            new_gcd_count[num] += 1
            
            # Extend with num
            for g in list(gcd_count.keys()):
                new_g = gcd(g, num)
                if new_g not in new_gcd_count:
                    new_gcd_count[new_g] = 0
                new_gcd_count[new_g] += gcd_count[g]
            
            gcd_count = new_gcd_count
        
        return gcd_count.get(target_gcd, 0)
    
    def _count_disjoint_pairs(self, nums, target_gcd):
        """Count pairs of disjoint non-empty subsequences both with GCD = target_gcd"""
        if not nums:
            return 0
        
        MOD = 10**9 + 7
        n = len(nums)
        
        # dp[i][g1][g2] = number of ways to assign first i elements such that:
        # - Some elements assigned to seq1 with GCD g1
        # - Some elements assigned to seq2 with GCD g2
        # - Remaining elements not assigned
        # We use None to represent "no subsequence yet"
        
        # This might be memory intensive. Let's use a different representation
        # dp[i][(g1, g2)] = count
        
        dp = {}
        dp[(None, None)] = 1  # Initially no elements assigned
        
        for num in nums:
            new_dp = {}
            
            for (g1, g2), count in dp.items():
                # Option 1: Don't include num
                key = (g1, g2)
                new_dp[key] = new_dp.get(key, 0) + count
                new_dp[key] %= MOD
                
                # Option 2: Include num in seq1
                new_g1 = gcd(g1, num) if g1 is not None else num
                key = (new_g1, g2)
                new_dp[key] = new_dp.get(key, 0) + count
                new_dp[key] %= MOD
                
                # Option 3: Include num in seq2
                new_g2 = gcd(g2, num) if g2 is not None else num
                key = (g1, new_g2)
                new_dp[key] = new_dp.get(key, 0) + count
                new_dp[key] %= MOD
            
            dp = new_dp
        
        # Count pairs where both g1 and g2 equal target_gcd
        result = dp.get((target_gcd, target_gcd), 0)
        return result
