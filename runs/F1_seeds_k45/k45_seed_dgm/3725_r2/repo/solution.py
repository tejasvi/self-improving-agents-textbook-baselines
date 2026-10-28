from typing import List
from collections import deque

class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        """
        Calculate the sum of minimum and maximum elements of all subarrays 
        with at most k elements.
        
        Approach:
        - For each starting position i, iterate through ending positions j
        - For each subarray [i..j] where j - i + 1 <= k, find min and max
        - Use deques to efficiently track min and max as we extend windows
        
        Time Complexity: O(n * k) where n is the length of nums
        Space Complexity: O(k) for the deques
        """
        result = 0
        n = len(nums)
        
        # For each starting position
        for i in range(n):
            # Deques to track indices of potential minimums and maximums
            # These deques will maintain indices in increasing order of their values
            min_deque = deque()  # monotonic increasing by value
            max_deque = deque()  # monotonic decreasing by value
            
            # For each ending position from start
            for j in range(i, min(i + k, n)):
                # Add current element to deques
                
                # Update min_deque
                while min_deque and nums[min_deque[-1]] >= nums[j]:
                    min_deque.pop()
                min_deque.append(j)
                
                # Update max_deque
                while max_deque and nums[max_deque[-1]] <= nums[j]:
                    max_deque.pop()
                max_deque.append(j)
                
                # Remove elements outside current window
                while min_deque and min_deque[0] < i:
                    min_deque.popleft()
                while max_deque and max_deque[0] < i:
                    max_deque.popleft()
                
                # Get min and max of current subarray [i..j]
                min_val = nums[min_deque[0]]
                max_val = nums[max_deque[0]]
                
                result += min_val + max_val
        
        return result
