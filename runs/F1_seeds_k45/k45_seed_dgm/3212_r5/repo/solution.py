from typing import List

class Solution:
    def numberOfGoodPartitions(self, nums: List[int]) -> int:
        """
        A good partition is one where no two subarrays contain the same number.
        
        Key insight: We can place a partition boundary after position i if and only if
        all numbers from 0 to i have their last occurrence at or before position i.
        
        In other words, we can partition after position i if:
        max_last_index_so_far == i
        
        If there are k valid internal partition points (not counting the end),
        then the total number of good partitions is 2^k.
        
        Algorithm:
        1. Find the last occurrence of each number
        2. Iterate through the array, tracking the maximum last occurrence index seen so far
        3. Count positions where max_last_index == current_index (valid partition points)
        4. Return 2^count mod (10^9 + 7)
        """
        MOD = 10**9 + 7
        
        # Find last occurrence of each number
        last_occurrence = {}
        for i, num in enumerate(nums):
            last_occurrence[num] = i
        
        # Count valid partition points
        partition_count = 0
        max_last_index = -1
        
        for i in range(len(nums)):
            max_last_index = max(max_last_index, last_occurrence[nums[i]])
            
            # If we can place a partition after position i
            if max_last_index == i:
                partition_count += 1
        
        # We always count the end position as a valid partition point,
        # but we want to count internal partitions (excluding the mandatory end)
        # Since we always have at least the end, we subtract 1
        partition_count -= 1
        
        # The number of good partitions is 2^partition_count
        return pow(2, partition_count, MOD)
