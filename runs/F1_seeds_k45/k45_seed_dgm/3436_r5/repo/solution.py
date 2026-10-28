from typing import List

class Solution:
    def minimumDifference(self, nums: List[int], k: int) -> int:
        """
        Find a subarray such that the absolute difference between k and the 
        bitwise OR of the subarray elements is minimized.
        
        Approach:
        - For each starting position, we can find all distinct OR values by 
          extending to the right
        - The key insight is that the number of distinct OR values is limited
          (at most ~30) because OR can only set bits, not unset them
        - Time complexity: O(n * 30) which is effectively O(n)
        """
        min_diff = float('inf')
        
        # Try each starting position
        for i in range(len(nums)):
            current_or = 0
            seen_ors = set()
            
            # Extend from position i to the right
            for j in range(i, len(nums)):
                current_or |= nums[j]
                
                # Only process if we haven't seen this OR value before
                # (optimization: skip duplicate OR values)
                if current_or not in seen_ors:
                    seen_ors.add(current_or)
                    diff = abs(k - current_or)
                    min_diff = min(min_diff, diff)
                    
                    # Early exit if we found exact match
                    if min_diff == 0:
                        return 0
        
        return min_diff
