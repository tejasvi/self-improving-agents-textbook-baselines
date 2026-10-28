from typing import List

class Solution:
    def maxIncreasingGroups(self, usageLimits: List[int]) -> int:
        """
        Return the maximum number of groups with strictly increasing lengths.
        
        Approach: Greedy with sorting
        
        Key insight: If we want to form k groups of sizes 1, 2, 3, ..., k,
        we need a total of 1+2+3+...+k = k*(k+1)/2 distinct elements.
        
        By sorting the usage limits in descending order and checking if we have
        enough total usage from the top i elements to form i groups, we can
        determine the maximum number of groups.
        
        Time Complexity: O(n log n) for sorting
        Space Complexity: O(n) for the sorted array
        """
        # Sort usage limits in descending order
        limits = sorted(usageLimits, reverse=True)
        
        groups = 0
        cumsum = 0
        
        for i, limit in enumerate(limits):
            # Accumulate the usage limit
            cumsum += limit
            
            # Check if we can form (i+1) groups using the top (i+1) elements
            # For (i+1) groups of sizes 1, 2, 3, ..., (i+1), we need:
            # (i+1) * (i+2) / 2 total elements
            needed = (i + 1) * (i + 2) // 2
            
            if cumsum >= needed:
                groups = i + 1
        
        return groups
