from typing import List

class Solution:
    def maxIncreasingGroups(self, usageLimits: List[int]) -> int:
        """
        Find the maximum number of groups with strictly increasing lengths.
        
        Strategy:
        1. Sort the usage limits in descending order
        2. Greedily form groups starting from size 1
        3. For each group of size k, take the k numbers with highest remaining limits
        4. Decrease their limits by 1 after using them
        5. Stop when we can't form a group of the next required size
        """
        
        # Sort in descending order to always use numbers with highest limits
        limits = sorted(usageLimits, reverse=True)
        
        group_count = 0
        group_size = 1  # The next group we want to form should have this size
        
        while True:
            # Check if we have enough elements with sufficient limits
            # We need group_size numbers with limit >= 1
            
            # Sum of the top group_size elements
            if group_size > len(limits):
                break
                
            total_available = sum(limits[:group_size])
            
            # We need at least group_size for this group
            if total_available < group_size:
                break
            
            # Form the group by using the top group_size numbers
            # Each is used once
            for i in range(group_size):
                limits[i] -= 1
            
            # Re-sort to maintain descending order for next iteration
            limits.sort(reverse=True)
            
            group_count += 1
            group_size += 1
        
        return group_count
