from typing import List

class Solution:
    def minimumDifference(self, nums: List[int], k: int) -> int:
        """
        Find a subarray such that the absolute difference between k and 
        the bitwise OR of the subarray elements is minimized.
        
        Approach:
        - For each position i, we maintain a set of distinct OR values
          for all subarrays ending at position i.
        - Key insight: OR operation is monotonic - as we extend subarrays
          to the left, OR values can only increase or stay the same.
        - The number of distinct OR values for subarrays ending at any position
          is at most O(log(max_element)) because each new element can add at most
          log bits worth of new values.
        
        Time Complexity: O(n * log(max_element) * log(n)) where we use a set
        Space Complexity: O(n * log(max_element)) for storing distinct OR values
        """
        min_diff = float('inf')
        
        # current_ors stores all distinct OR values for subarrays ending at current position
        current_ors = set()
        
        for num in nums:
            # New set for subarrays ending at this position
            new_ors = {num}  # subarray containing just this element
            
            # Extend all previous subarrays by including current element
            for prev_or in current_ors:
                new_ors.add(prev_or | num)
            
            current_ors = new_ors
            
            # Check all OR values for subarrays ending at current position
            for or_value in current_ors:
                diff = abs(k - or_value)
                min_diff = min(min_diff, diff)
                
                # Early termination if we found exact match
                if min_diff == 0:
                    return 0
        
        return min_diff
