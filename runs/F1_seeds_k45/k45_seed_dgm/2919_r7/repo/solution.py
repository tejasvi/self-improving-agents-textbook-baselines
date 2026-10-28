from typing import List

class Solution:
    def maxIncreasingGroups(self, usageLimits: List[int]) -> int:
        """
        Find the maximum number of groups with increasing length.
        
        Strategy:
        - Sort usage limits in descending order (greedy approach)
        - Try to form groups of size 1, 2, 3, ... using numbers with highest available limits
        - For each group of size k, use the k numbers with the highest remaining usage limits
        """
        # Sort in descending order to prioritize using numbers with higher limits
        limits = sorted(usageLimits, reverse=True)
        
        group_count = 0
        group_size = 1
        
        while True:
            # Check if we can form a group of size `group_size`
            # We need group_size numbers with remaining limit >= 1
            
            # Count how many numbers have limit > 0 (can be used)
            available_count = sum(1 for limit in limits if limit > 0)
            
            if available_count < group_size:
                # Can't form the next group
                break
            
            # Greedily take the top group_size numbers with highest limits
            # and decrement their limits
            used = 0
            for i in range(len(limits)):
                if used < group_size:
                    if limits[i] > 0:
                        limits[i] -= 1
                        used += 1
            
            if used < group_size:
                # Couldn't use enough numbers
                break
            
            # Successfully formed a group
            group_count += 1
            group_size += 1
        
        return group_count
