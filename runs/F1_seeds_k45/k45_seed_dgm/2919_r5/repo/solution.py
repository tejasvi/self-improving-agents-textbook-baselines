from typing import List

class Solution:
    def maxIncreasingGroups(self, usageLimits: List[int]) -> int:
        """
        Find the maximum number of groups with strictly increasing lengths
        where each number i can be used at most usageLimits[i] times.
        
        Strategy:
        1. Sort usage limits in descending order
        2. Try to create groups of size 1, 2, 3, 4, ... greedily
        3. For each group, use the numbers with the highest remaining usage limits
        4. Stop when we don't have enough numbers for the next group
        """
        # Sort in descending order to greedily pick the most available numbers
        limits = sorted(usageLimits, reverse=True)
        
        groups = 0
        group_size = 1
        
        while True:
            # Check if we can form a group of size group_size
            # We need group_size numbers, so we take the top group_size elements
            # and reduce each by 1
            
            total = 0
            for i in range(group_size):
                if i >= len(limits):
                    # Not enough distinct numbers
                    return groups
                total += limits[i]
            
            if total < group_size:
                # Not enough usage remaining to form this group
                return groups
            
            # We can form this group, so:
            # 1. Increment group count
            # 2. Reduce the usage of the top group_size elements
            # 3. Re-sort to prepare for the next iteration
            groups += 1
            
            # Reduce usage limits
            for i in range(group_size):
                limits[i] -= 1
            
            # Re-sort in descending order
            limits.sort(reverse=True)
            
            # Prepare for next group
            group_size += 1
