from typing import List

class Solution:
    def sumOfPower(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        nums.sort()
        n = len(nums)
        result = 0
        
        # For each position j (as the maximum)
        for j in range(n):
            # For each position i (as the minimum, i <= j)
            for i in range(j + 1):
                # Number of elements between i and j (exclusive)
                between = j - i - 1
                
                # We need to count groups where:
                # - nums[i] is the minimum
                # - nums[j] is the maximum
                # - We can include/exclude any subset of elements between i and j
                
                # Number of such groups = 2^between
                # (each element between can be included or not)
                
                count = pow(2, between, MOD)
                
                # Power contribution = nums[j]^2 * nums[i]
                power = (nums[j] * nums[j] % MOD) * nums[i] % MOD
                
                # Add to result
                result = (result + count * power) % MOD
        
        return result
