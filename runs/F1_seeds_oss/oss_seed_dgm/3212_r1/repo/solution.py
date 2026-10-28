from typing import List

MOD = 10**9 + 7

class Solution:
    def numberOfGoodPartitions(self, nums: List[int]) -> int:
        """Return number of good partitions modulo 1e9+7.
        A partition is good if each distinct value appears in at most one subarray.
        The array can be divided into minimal blocks where the last occurrence of any
        element seen so far defines the block boundary. The number of good partitions
        equals 2^{(number_of_blocks - 1)}.
        """
        n = len(nums)
        # Record the last occurrence index for each number
        last = {}
        for i, x in enumerate(nums):
            last[x] = i
        blocks = 0
        cur_max = -1
        for i, x in enumerate(nums):
            cur_max = max(cur_max, last[x])
            # When current index reaches the furthest last occurrence of any number
            # seen in this segment, we can close a block.
            if i == cur_max:
                blocks += 1
        # Number of ways to merge adjacent blocks: each of the (blocks-1) gaps can be
        # either cut or not.
        return pow(2, blocks - 1, MOD)
