from typing import List

MOD = 10**9 + 7

class Solution:
    def numberOfGoodPartitions(self, nums: List[int]) -> int:
        """Return the number of good partitions of the array.

        A partition is good if no integer appears in more than one subarray.
        The answer equals 2^{k-1} where k is the number of minimal blocks
        obtained by merging the occurrence intervals of each distinct number.
        """
        # Record the last index where each value appears.
        last_occurrence = {}
        for i, v in enumerate(nums):
            last_occurrence[v] = i

        blocks = 0
        cur_max = -1
        for i, v in enumerate(nums):
            cur_max = max(cur_max, last_occurrence[v])
            # When current index reaches the furthest last occurrence of any
            # number seen so far, we can finish a minimal block here.
            if i == cur_max:
                blocks += 1
        # Number of ways to optionally merge adjacent minimal blocks.
        # There are (blocks-1) possible cut positions; each can be kept or removed.
        # Hence answer = 2^{blocks-1}.
        if blocks == 0:
            return 0
        return pow(2, blocks - 1, MOD)
