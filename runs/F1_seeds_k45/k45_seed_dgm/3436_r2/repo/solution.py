from typing import List


class Solution:
    def minimumDifference(self, nums: List[int], k: int) -> int:
        """
        Find a subarray such that the absolute difference between k and 
        the bitwise OR of the subarray elements is minimized.
        
        Key insight: The bitwise OR is monotonically increasing as we add more elements.
        Since there are at most 30 bits in a number up to 10^9, there are at most
        30 distinct OR values for subarrays starting at any position.
        
        Algorithm:
        1. For each starting position i, compute OR values for all subarrays [i, j]
        2. Since OR can only increase and there are at most 30 distinct values,
           we efficiently find all possible OR values
        3. Track the minimum difference from k
        """
        min_diff = float('inf')
        
        # Try all starting positions
        for i in range(len(nums)):
            current_or = 0
            # For each starting position, find all distinct OR values
            # by extending the subarray to the right
            for j in range(i, len(nums)):
                current_or |= nums[j]
                # Calculate the difference and update minimum
                diff = abs(k - current_or)
                min_diff = min(min_diff, diff)
                
                # Early termination: if we found 0 difference, we can't do better
                if min_diff == 0:
                    return 0
        
        return min_diff
