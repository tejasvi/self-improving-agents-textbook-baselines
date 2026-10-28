from typing import List


class Solution:
    def minimumDifference(self, nums: List[int], k: int) -> int:
        """
        Find a subarray with bitwise OR closest to k.
        
        Key insight: For each starting position i, as we extend the subarray,
        the OR values can only increase (or stay same). Since each element has
        at most 30 bits, there are at most 30 distinct OR values for any
        starting position. This gives us O(n * log(max_value)) complexity.
        """
        min_diff = float('inf')
        
        for i in range(len(nums)):
            # For each starting position, track unique OR values
            unique_ors = set()
            current_or = 0
            
            for j in range(i, len(nums)):
                current_or |= nums[j]
                
                # Only process if we haven't seen this OR value before
                # (optimization: if OR doesn't change, we've seen this value)
                if current_or not in unique_ors:
                    unique_ors.add(current_or)
                    diff = abs(k - current_or)
                    min_diff = min(min_diff, diff)
                    
                    # Early termination: if we found exact match, we can't do better
                    if min_diff == 0:
                        return 0
        
        return min_diff
