from typing import List

class Solution:
    def minimumDifference(self, nums: List[int], k: int) -> int:
        """
        Find a subarray with bitwise OR closest to k.
        
        Approach:
        - For each starting position i, we iterate through ending positions j.
        - For efficiency, we maintain only the distinct OR values that can be 
          formed by subarrays nums[i..j] for a fixed i as j varies.
        - Key insight: The number of distinct OR values is limited to at most ~30
          (the number of bits in an integer), because OR can only set bits, never unset them.
        
        Time Complexity: O(n * log(max_num)) where max_num is ~10^9
        Space Complexity: O(log(max_num)) for the set of distinct OR values
        """
        min_diff = float('inf')
        
        # For each starting position
        for i in range(len(nums)):
            # Track distinct OR values for subarrays starting at position i
            or_value = 0
            
            # Expand from position i to the right
            for j in range(i, len(nums)):
                # OR the current element
                or_value |= nums[j]
                
                # Calculate the difference with k
                diff = abs(k - or_value)
                min_diff = min(min_diff, diff)
        
        return min_diff
