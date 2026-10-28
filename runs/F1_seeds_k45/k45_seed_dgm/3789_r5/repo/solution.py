from typing import List

class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        """
        For each possible removal of one conflicting pair, count valid subarrays.
        A subarray is valid if it doesn't contain both elements of any remaining conflicting pair.
        
        Approach:
        - Total subarrays = n * (n + 1) / 2
        - For each conflicting pair (a, b) that remains, subtract subarrays containing both
        - Use inclusion-exclusion principle for multiple pairs
        """
        
        def count_valid_subarrays(remaining_pairs):
            """
            Count subarrays that don't contain both a and b for any pair (a,b).
            Using inclusion-exclusion principle.
            """
            if not remaining_pairs:
                return n * (n + 1) // 2
            
            # Total subarrays
            total = n * (n + 1) // 2
            
            # We need to subtract subarrays that violate at least one constraint
            # Using inclusion-exclusion
            
            # Count invalid subarrays using bitmask
            invalid_count = 0
            m = len(remaining_pairs)
            
            # Iterate through all non-empty subsets of pairs
            for mask in range(1, 1 << m):
                # Find the union of ranges that must be covered
                min_pos = 1
                max_pos = 0
                
                count = 0
                for i in range(m):
                    if mask & (1 << i):
                        a, b = remaining_pairs[i]
                        min_elem = min(a, b)
                        max_elem = max(a, b)
                        min_pos = max(min_pos, min_elem)
                        max_pos = max(max_pos, max_elem)
                        count += 1
                
                # A subarray must contain all required ranges
                if min_pos <= max_pos:
                    # Count subarrays that contain [min_pos, max_pos]
                    # Start position can be 1 to min_pos, end position can be max_pos to n
                    num_subarrays = min_pos * (n - max_pos + 1)
                    
                    # Apply inclusion-exclusion
                    if count % 2 == 1:
                        invalid_count += num_subarrays
                    else:
                        invalid_count -= num_subarrays
            
            return total - invalid_count
        
        max_count = 0
        
        # Try removing each conflicting pair
        for remove_idx in range(len(conflictingPairs)):
            remaining = [conflictingPairs[i] for i in range(len(conflictingPairs)) if i != remove_idx]
            count = count_valid_subarrays(remaining)
            max_count = max(max_count, count)
        
        return max_count
