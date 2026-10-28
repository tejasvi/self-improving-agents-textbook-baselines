from typing import List

class Solution:
    def sumOfPower(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        nums.sort()
        n = len(nums)
        result = 0
        
        # For each position i, treat nums[i] as the minimum
        for i in range(n):
            # For each position j >= i, treat nums[j] as the maximum
            for j in range(i, n):
                # Number of subsets where nums[i] is min and nums[j] is max
                # We can choose any subset of elements between i+1 and j-1
                # That's 2^(j-i-1) subsets
                num_subsets = pow(2, j - i - 1, MOD)
                
                # Power of each such group is nums[j]^2 * nums[i]
                power = (nums[j] * nums[j] % MOD) * nums[i] % MOD
                
                # Add contribution of all such subsets
                result = (result + power * num_subsets) % MOD
        
        return result
