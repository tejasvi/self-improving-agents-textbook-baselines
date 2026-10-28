from typing import List

class Solution:
    def sumOfPower(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        
        # Sort the array
        nums.sort()
        n = len(nums)
        result = 0
        
        # For each element, we'll consider it as the minimum of groups
        # and iterate through possible maximums
        for i in range(n):
            min_val = nums[i]
            
            # For each element at index j >= i, consider it as the maximum
            for j in range(i, n):
                max_val = nums[j]
                
                # Now we need to count how many subsets have:
                # - min_val as minimum
                # - max_val as maximum
                # - both min_val and max_val in the group
                # - any subset of elements between i+1 and j-1
                
                if j == i:
                    # Single element group
                    power = (max_val * max_val % MOD) * min_val % MOD
                    result = (result + power) % MOD
                else:
                    # Multiple element group
                    # Elements between i and j can be included or not (except i and j must be included)
                    # Count of such subsets = 2^(j-i-1)
                    count_between = j - i - 1
                    num_subsets = pow(2, count_between, MOD)
                    
                    power = (max_val * max_val % MOD) * min_val % MOD
                    contribution = (power * num_subsets) % MOD
                    result = (result + contribution) % MOD
        
        return result
