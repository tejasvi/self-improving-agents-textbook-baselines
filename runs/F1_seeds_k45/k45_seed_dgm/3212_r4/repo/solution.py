from typing import List

class Solution:
    def numberOfGoodPartitions(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        
        # Find the last occurrence of each number
        last_occurrence = {}
        for i, num in enumerate(nums):
            last_occurrence[num] = i
        
        # Count the number of positions where we can place a partition boundary
        partition_count = 0
        max_last_occurrence = -1
        
        for i, num in enumerate(nums):
            # Update the maximum last occurrence seen so far
            max_last_occurrence = max(max_last_occurrence, last_occurrence[num])
            
            # If current position is the maximum last occurrence,
            # we can place a partition boundary here
            if i == max_last_occurrence:
                partition_count += 1
        
        # The total number of good partitions is 2^(partition_count - 1)
        # We subtract 1 because the last partition boundary is fixed at the end
        return pow(2, partition_count - 1, MOD)
