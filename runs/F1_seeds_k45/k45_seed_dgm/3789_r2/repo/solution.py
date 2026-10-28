from typing import List

class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        """
        Count the number of valid subarrays after removing one conflicting pair.
        
        A subarray is valid if it doesn't contain both elements of any conflicting pair.
        
        Total subarrays = n * (n + 1) / 2
        For each remaining pair [a, b], subtract subarrays containing both:
        - If a < b: subarrays starting at position <= a and ending at position >= b
        - Count = a * (n - b + 1)
        """
        
        def count_valid_subarrays(pairs):
            """Count valid subarrays given a set of conflicting pairs"""
            if not pairs:
                return n * (n + 1) // 2
            
            total = n * (n + 1) // 2
            
            # Subtract subarrays that contain both elements for each conflicting pair
            for a, b in pairs:
                # Ensure a < b
                if a > b:
                    a, b = b, a
                
                # Number of subarrays containing both a and b
                # These are subarrays that start at position <= a and end at position >= b
                # Start positions: 1 to a (a choices)
                # End positions: b to n (n - b + 1 choices)
                invalid_count = a * (n - b + 1)
                total -= invalid_count
            
            return total
        
        max_subarrays = 0
        
        # Try removing each conflicting pair
        for i in range(len(conflictingPairs)):
            # Create a new list without the pair at index i
            remaining_pairs = conflictingPairs[:i] + conflictingPairs[i+1:]
            
            # Count valid subarrays with this pair removed
            valid_count = count_valid_subarrays(remaining_pairs)
            max_subarrays = max(max_subarrays, valid_count)
        
        return max_subarrays
