from typing import List

class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        """
        Calculate the sum of (min + max) for all subarrays with at most k elements.
        
        Approach:
        - For each starting position i, iterate through all ending positions j
          where the subarray length is at most k
        - Track the running minimum and maximum as we extend the window
        - Add (min + max) to the result for each subarray
        
        Time Complexity: O(n*k)
        Space Complexity: O(1)
        """
        result = 0
        n = len(nums)
        
        # Iterate through each starting position
        for i in range(n):
            min_val = nums[i]
            max_val = nums[i]
            
            # For each starting position i, iterate through all ending positions j
            # where subarray length is at most k
            for j in range(i, min(i + k, n)):
                # Update min and max with the new element at position j
                min_val = min(min_val, nums[j])
                max_val = max(max_val, nums[j])
                
                # Add the sum of min and max for this subarray
                result += min_val + max_val
        
        return result
