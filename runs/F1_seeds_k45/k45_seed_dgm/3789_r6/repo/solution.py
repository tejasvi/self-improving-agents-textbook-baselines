from typing import List

class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        """
        Remove exactly one conflicting pair and maximize the number of valid subarrays
        that don't contain both elements of any remaining conflicting pair.
        """
        
        def count_invalid_subarrays(pairs):
            """
            Count subarrays that contain both elements of at least one conflicting pair.
            Uses inclusion-exclusion principle.
            """
            if not pairs:
                return 0
            
            # For efficiency, we'll use a different approach
            # Count directly by checking each pair's contribution
            
            invalid_count = 0
            
            for a, b in pairs:
                if a > b:
                    a, b = b, a
                
                # Number of subarrays containing both a and b
                # Start position: 1 to a, End position: b to n
                # Total = a * (n - b + 1)
                invalid_count += a * (n - b + 1)
            
            # For inclusion-exclusion, we need to subtract overlaps
            # Two pairs [a,b] and [c,d] have overlap if a subarray contains all 4 elements
            # This is complex, so we use a simpler enumeration approach for correctness
            
            # Actually, let's use a simpler but still efficient approach:
            # Use DP or direct enumeration for small n or optimize with observation
            
            # For now, use direct counting with optimization
            return invalid_count
        
        def count_valid_subarrays_direct(pairs):
            """
            Count valid subarrays by enumerating all subarrays and checking constraints.
            """
            total = n * (n + 1) // 2
            
            if not pairs:
                return total
            
            # For each pair, count subarrays that violate it
            # Use inclusion-exclusion
            
            # Convert to more efficient format: set of (min, max) for each pair
            pair_set = set()
            for a, b in pairs:
                if a > b:
                    a, b = b, a
                pair_set.add((a, b))
            
            invalid = 0
            
            # Iterate through all possible subarrays
            for start in range(1, n + 1):
                for end in range(start, n + 1):
                    # Check if this subarray violates any constraint
                    violates = False
                    for a, b in pair_set:
                        if start <= a <= end and start <= b <= end:
                            violates = True
                            break
                    if violates:
                        invalid += 1
            
            return total - invalid
        
        max_count = 0
        
        # Try removing each conflicting pair
        for i in range(len(conflictingPairs)):
            # Create a new list without the i-th pair
            remaining_pairs = conflictingPairs[:i] + conflictingPairs[i+1:]
            
            # Count valid subarrays with this configuration
            count = count_valid_subarrays_direct(remaining_pairs)
            max_count = max(max_count, count)
        
        return max_count
