from typing import List

class Solution:
    def sumOfPower(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        nums.sort()
        n = len(nums)
        result = 0
        
        # For each element as the maximum
        for j in range(n):
            max_val = nums[j]
            max_sq = (max_val * max_val) % MOD
            
            # For each element as the minimum
            for i in range(j + 1):
                min_val = nums[i]
                
                # Count elements between i and j (exclusive)
                # These elements can be included or excluded: 2^(j-i-1) ways
                # But if j == i, there's only 1 way (just the element itself)
                between_count = j - i - 1
                
                # Number of subsets with nums[i] as min and nums[j] as max
                # = 2^(j-i-1) (we must include nums[i] and nums[j])
                num_subsets = pow(2, between_count, MOD)
                
                # Add contribution: num_subsets * max_val^2 * min_val
                contribution = (num_subsets * max_sq % MOD) * min_val % MOD
                result = (result + contribution) % MOD
        
        return result
