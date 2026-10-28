from collections import deque
from typing import List

class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        """
        Calculate the sum of maximum and minimum elements of all subarrays with at most k elements.
        
        Args:
            nums: List of integers
            k: Maximum size of subarrays
            
        Returns:
            Sum of (min + max) for all subarrays of size 1 to k
        """
        n = len(nums)
        result = 0
        
        # For each starting position
        for start in range(n):
            # Use deques to maintain indices of min and max elements
            min_deque = deque()  # stores indices, maintaining increasing values
            max_deque = deque()  # stores indices, maintaining decreasing values
            
            # For each ending position (at most k elements from start)
            for end in range(start, min(start + k, n)):
                # Update min_deque
                # Remove indices of elements >= current element from the back
                while min_deque and nums[min_deque[-1]] >= nums[end]:
                    min_deque.pop()
                min_deque.append(end)
                
                # Update max_deque
                # Remove indices of elements <= current element from the back
                while max_deque and nums[max_deque[-1]] <= nums[end]:
                    max_deque.pop()
                max_deque.append(end)
                
                # Remove indices that are out of current window
                while min_deque and min_deque[0] < start:
                    min_deque.popleft()
                while max_deque and max_deque[0] < start:
                    max_deque.popleft()
                
                # Add min and max of current subarray
                min_val = nums[min_deque[0]]
                max_val = nums[max_deque[0]]
                result += min_val + max_val
        
        return result
