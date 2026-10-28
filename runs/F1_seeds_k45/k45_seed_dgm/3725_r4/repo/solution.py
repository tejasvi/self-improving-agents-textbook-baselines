from typing import List

class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        """
        Find the sum of maximum and minimum elements of all subarrays with at most k elements.
        
        Args:
            nums: List of integers
            k: Maximum size of subarrays
            
        Returns:
            Sum of (min + max) for all subarrays of size at most k
        """
        result = 0
        n = len(nums)
        
        # For each starting position
        for i in range(n):
            min_val = nums[i]
            max_val = nums[i]
            
            # For each ending position (at most k elements in subarray)
            for j in range(i, min(i + k, n)):
                # Update min and max for subarray nums[i:j+1]
                min_val = min(min_val, nums[j])
                max_val = max(max_val, nums[j])
                
                # Add min and max to result
                result += min_val + max_val
        
        return result
