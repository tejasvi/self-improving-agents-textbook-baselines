class Solution:
    def maxIncreasingGroups(self, usageLimits: List[int]) -> int:
        # Sort in descending order to greedily use numbers with highest limits
        limits = sorted(usageLimits, reverse=True)
        
        groups = 0
        group_size = 1
        
        while group_size <= len(limits):
            # Check if sum of top 'group_size' limits is >= group_size
            # This ensures we can form a group of this size
            top_sum = sum(limits[:group_size])
            
            if top_sum < group_size:
                break
            
            # We can form this group
            # Subtract 1 from each of the top 'group_size' elements
            for i in range(group_size):
                limits[i] -= 1
            
            # Re-sort to maintain descending order for next iteration
            limits.sort(reverse=True)
            
            groups += 1
            group_size += 1
        
        return groups
