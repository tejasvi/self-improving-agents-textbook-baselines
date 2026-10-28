from typing import List

class Solution:
    def numberOfGoodPartitions(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        
        # Find the last occurrence of each number
        last_occurrence = {}
        for i, num in enumerate(nums):
            last_occurrence[num] = i
        
        # Find positions where we can make a partition
        # A partition can be made at position i if i is the rightmost position
        # of all distinct numbers seen so far
        partition_points = []
        max_right = 0
        
        for i in range(len(nums)):
            # Update the rightmost position we need to see for numbers up to i
            max_right = max(max_right, last_occurrence[nums[i]])
            
            # If current position is the rightmost, we can partition here
            if i == max_right:
                partition_points.append(i)
        
        # If we have k partition points, we can make 2^(k-1) good partitions
        # because we can choose to include or exclude each internal boundary
        # (except the last boundary which must be included)
        k = len(partition_points)
        if k == 0:
            return 1
        
        # The answer is 2^(k-1) mod MOD
        return pow(2, k - 1, MOD)
