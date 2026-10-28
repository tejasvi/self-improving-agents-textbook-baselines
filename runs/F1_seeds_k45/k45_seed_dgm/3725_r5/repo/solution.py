from typing import List
from collections import deque

class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        """
        Calculate the sum of maximum and minimum elements of all subarrays 
        with at most k elements.
        
        Args:
            nums: List of integers
            k: Maximum subarray length
            
        Returns:
            Sum of all min and max elements from all valid subarrays
        """
        n = len(nums)
        result = 0
        
        # For each starting position
        for i in range(n):
            # Use deques to efficiently track min and max
            min_deque = deque()  # stores indices in increasing order of values
            max_deque = deque()  # stores indices in increasing order of values
            
            # For each possible length (1 to k)
            for j in range(i, min(i + k, n)):
                # Add nums[j] to the deques
                
                # Update min_deque - keep it in increasing order
                while min_deque and nums[min_deque[-1]] >= nums[j]:
                    min_deque.pop()
                min_deque.append(j)
                
                # Update max_deque - keep it in decreasing order
                while max_deque and nums[max_deque[-1]] <= nums[j]:
                    max_deque.pop()
                max_deque.append(j)
                
                # Remove elements outside current window [i, j]
                while min_deque and min_deque[0] < i:
                    min_deque.popleft()
                while max_deque and max_deque[0] < i:
                    max_deque.popleft()
                
                # Add min and max to result
                min_val = nums[min_deque[0]]
                max_val = nums[max_deque[0]]
                result += min_val + max_val
        
        return result
