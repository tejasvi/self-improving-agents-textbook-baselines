from typing import List

class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        """
        Given an array nums with numbers 1 to n, and conflicting pairs,
        remove exactly one conflicting pair and count the maximum number of
        non-empty subarrays that don't contain both elements of any remaining pair.
        """
        
        def count_bad_subarrays(a, b, n):
            """
            Count subarrays that contain both a and b (where a < b).
            If a < b, we need subarrays that start at or before a and end at or after b.
            Number of such subarrays = a * (n + 1 - b)
            """
            if a > b:
                a, b = b, a
            return a * (n + 1 - b)
        
        def count_valid_subarrays(remaining_pairs, n):
            """
            Count subarrays that don't contain both elements of any pair in remaining_pairs.
            Use inclusion-exclusion principle.
            """
            if not remaining_pairs:
                # No constraints, all subarrays are valid
                return n * (n + 1) // 2
            
            # Normalize pairs (ensure a < b)
            pairs = []
            for a, b in remaining_pairs:
                if a > b:
                    a, b = b, a
                pairs.append((a, b))
            
            # Use inclusion-exclusion
            total = n * (n + 1) // 2
            bad_subarrays = set()
            
            # Single pairs
            for a, b in pairs:
                bad_subarrays.add((a, b))
            
            # We need to subtract bad subarrays using inclusion-exclusion
            # For efficiency with large numbers of pairs, we need a smarter approach
            
            # Calculate using DP or direct counting
            # A subarray [i, j] is valid if it doesn't contain both elements of any pair
            
            valid = 0
            for i in range(1, n + 1):
                for j in range(i, n + 1):
                    # Check if subarray [i, j] is valid
                    is_valid = True
                    for a, b in pairs:
                        if i <= a <= j and i <= b <= j:
                            is_valid = False
                            break
                    if is_valid:
                        valid += 1
            
            return valid
        
        # Try removing each pair and find the maximum valid subarrays
        max_valid = 0
        
        for idx in range(len(conflictingPairs)):
            # Create remaining pairs by excluding index idx
            remaining = [conflictingPairs[i] for i in range(len(conflictingPairs)) if i != idx]
            valid = count_valid_subarrays(remaining, n)
            max_valid = max(max_valid, valid)
        
        return max_valid
