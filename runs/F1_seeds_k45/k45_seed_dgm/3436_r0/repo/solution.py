from typing import List

class Solution:
    def minimumDifference(self, nums: List[int], k: int) -> int:
        """
        Find a subarray with bitwise OR closest to k.
        
        The key insight is that for each position i, we maintain all distinct OR values
        for subarrays ending at position i. Due to the nature of OR operations, once a 
        bit is set to 1, it remains 1. This means the number of distinct OR values for 
        subarrays ending at position i is at most O(log(max_value)) ≈ 30.
        
        Args:
            nums: List of positive integers
            k: Target value
            
        Returns:
            Minimum absolute difference between k and any subarray's OR value
        """
        min_diff = float('inf')
        
        # For each ending position, maintain the set of distinct OR values
        # that can be achieved by subarrays ending at that position
        current_or_values = set()
        
        for num in nums:
            # New set of OR values for subarrays ending at current position
            new_or_values = {num}  # subarray containing just current element
            
            # OR current element with all previous OR values
            for prev_or in current_or_values:
                new_or_values.add(prev_or | num)
            
            current_or_values = new_or_values
            
            # Calculate minimum difference for all OR values ending at current position
            for or_value in current_or_values:
                diff = abs(k - or_value)
                min_diff = min(min_diff, diff)
                
                # Early termination if we find exact match
                if min_diff == 0:
                    return 0
        
        return min_diff
