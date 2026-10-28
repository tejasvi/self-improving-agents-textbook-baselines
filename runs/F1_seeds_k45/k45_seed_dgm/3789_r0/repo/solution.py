from typing import List

class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        """
        Count valid subarrays after removing exactly one conflicting pair.
        A valid subarray doesn't contain both elements of any remaining conflicting pair.
        """
        max_count = 0
        
        # Try removing each conflicting pair one at a time
        for remove_idx in range(len(conflictingPairs)):
            # Create the remaining pairs
            remaining_pairs = [
                pair for i, pair in enumerate(conflictingPairs) 
                if i != remove_idx
            ]
            
            # Count valid subarrays for this configuration
            count = self.countValidSubarrays(n, remaining_pairs)
            max_count = max(max_count, count)
        
        return max_count
    
    def countValidSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        """
        Count the number of subarrays that don't contain both elements
        of any conflicting pair.
        
        Using inclusion-exclusion principle:
        - Start with all subarrays
        - Subtract subarrays that contain each conflicting pair
        - Add back subarrays that contain multiple conflicting pairs (to avoid double counting)
        """
        if not conflictingPairs:
            # No conflicting pairs, all subarrays are valid
            return n * (n + 1) // 2
        
        # Total subarrays
        total = n * (n + 1) // 2
        
        # Use inclusion-exclusion to count invalid subarrays
        invalid_count = 0
        
        # Count subarrays containing at least one complete conflicting pair
        # We'll use a different approach: for each subset of pairs, 
        # count subarrays that contain ALL pairs in that subset
        
        from itertools import combinations
        
        for r in range(1, len(conflictingPairs) + 1):
            for pair_combo in combinations(range(len(conflictingPairs)), r):
                # Find the range [min_val, max_val] that must be in the subarray
                # to contain all pairs in this combination
                min_val = float('inf')
                max_val = float('-inf')
                
                for idx in pair_combo:
                    a, b = conflictingPairs[idx]
                    min_val = min(min_val, a, b)
                    max_val = max(max_val, a, b)
                
                # Count subarrays [i, j] where i <= min_val and j >= max_val
                # i can be from 1 to min_val (inclusive)
                # j can be from max_val to n (inclusive)
                count = min_val * (n - max_val + 1)
                
                # Apply inclusion-exclusion
                if r % 2 == 1:
                    invalid_count += count
                else:
                    invalid_count -= count
        
        return total - invalid_count
