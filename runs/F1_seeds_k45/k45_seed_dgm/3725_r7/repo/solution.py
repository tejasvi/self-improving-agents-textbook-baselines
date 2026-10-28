from collections import deque
from typing import List

class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        """
        Calculate the sum of max and min elements of all subarrays with at most k elements.
        
        For each subarray length from 1 to k:
        - Use sliding window with deques to track min and max efficiently
        - Add sum of all mins and maxs to result
        """
        result = 0
        n = len(nums)
        
        # For each subarray length from 1 to k
        for length in range(1, k + 1):
            # Use deques to maintain indices of potential min/max candidates
            # For minimum values
            min_deque = deque()
            # For maximum values
            max_deque = deque()
            
            # Initialize deques with first window
            for i in range(length):
                # Maintain min deque in increasing order of values
                while min_deque and nums[min_deque[-1]] >= nums[i]:
                    min_deque.pop()
                min_deque.append(i)
                
                # Maintain max deque in decreasing order of values
                while max_deque and nums[max_deque[-1]] <= nums[i]:
                    max_deque.pop()
                max_deque.append(i)
            
            # First window
            result += nums[min_deque[0]] + nums[max_deque[0]]
            
            # Slide the window
            for i in range(length, n):
                # Remove elements outside the current window
                if min_deque and min_deque[0] <= i - length:
                    min_deque.popleft()
                if max_deque and max_deque[0] <= i - length:
                    max_deque.popleft()
                
                # Add new element to deques
                while min_deque and nums[min_deque[-1]] >= nums[i]:
                    min_deque.pop()
                min_deque.append(i)
                
                while max_deque and nums[max_deque[-1]] <= nums[i]:
                    max_deque.pop()
                max_deque.append(i)
                
                # Add min and max of current window
                result += nums[min_deque[0]] + nums[max_deque[0]]
        
        return result
