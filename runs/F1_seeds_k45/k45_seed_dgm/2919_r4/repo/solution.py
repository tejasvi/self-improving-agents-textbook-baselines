class Solution:
    def maxIncreasingGroups(self, usageLimits: List[int]) -> int:
        # Sort the usage limits in descending order
        # We'll greedily try to form groups of sizes 1, 2, 3, ...
        usageLimits.sort(reverse=True)
        
        groups = 0
        next_group_size = 1
        
        while True:
            # Try to form a group of size next_group_size
            # We need to check if we have enough numbers with remaining usage >= 1
            
            # Count how many numbers have usage >= 1
            available_count = 0
            for i in range(len(usageLimits)):
                if usageLimits[i] > 0:
                    available_count += 1
            
            # If we can't form a group of size next_group_size, stop
            if available_count < next_group_size:
                break
            
            # Form a group by using the next_group_size numbers with highest usage
            # We greedily pick the top next_group_size numbers and use one from each
            count_used = 0
            for i in range(len(usageLimits)):
                if count_used >= next_group_size:
                    break
                if usageLimits[i] > 0:
                    usageLimits[i] -= 1
                    count_used += 1
            
            groups += 1
            next_group_size += 1
        
        return groups
