from typing import List

class Solution:
    def numberOfGoodPartitions(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        
        # Find the last occurrence of each number
        last_occurrence = {}
        for i, num in enumerate(nums):
            last_occurrence[num] = i
        
        # Count valid partitions
        # We can place a partition boundary at position i if:
        # - All distinct elements from start of current chunk to i 
        #   have their last occurrence at or before i
        
        count = 1  # Start with 1 way (the entire array as one partition)
        max_reach = 0
        
        for i in range(n):
            # Update max_reach to the furthest position we need to go
            max_reach = max(max_reach, last_occurrence[nums[i]])
            
            # If we can partition here (all elements in current chunk are "closed")
            if i == max_reach and i < n - 1:  # Don't double count the final partition
                count = (count * 2) % MOD
        
        return count
