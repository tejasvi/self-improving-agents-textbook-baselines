from typing import List


class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        """
        Calculate the sum of maximum and minimum elements of all subarrays with at most k elements.
        
        Args:
            nums: List of integers
            k: Maximum subarray size
            
        Returns:
            Sum of (min + max) for all subarrays with at most k elements
        """
        result = 0
        n = len(nums)
        
        # For each starting position
        for i in range(n):
            min_val = nums[i]
            max_val = nums[i]
            
            # For each possible ending position (at most k elements)
            for j in range(i, min(i + k, n)):
                min_val = min(min_val, nums[j])
                max_val = max(max_val, nums[j])
                
                # Add min + max for subarray [i, j]
                result += min_val + max_val
        
        return result
