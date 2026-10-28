from typing import List

class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        """
        Calculate sum of min and max of all subarrays with at most k elements.
        
        Args:
            nums: List of integers
            k: Maximum size of subarrays to consider
        
        Returns:
            Sum of all minimum and maximum elements across all subarrays with at most k elements
        """
        n = len(nums)
        result = 0
        
        # For each starting position
        for i in range(n):
            min_val = nums[i]
            max_val = nums[i]
            
            # For each ending position (subarray length from 1 to k)
            for j in range(i, min(i + k, n)):
                # Update min and max with the new element at position j
                min_val = min(min_val, nums[j])
                max_val = max(max_val, nums[j])
                
                # Add min and max of subarray [i, j]
                result += min_val + max_val
        
        return result
