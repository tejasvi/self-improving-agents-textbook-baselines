from typing import List


class Solution:
    def numberOfGoodPartitions(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        last = {}
        for i, x in enumerate(nums):
            last[x] = i
        # Count the number of valid cut positions: after index i, no value
        # may appear both at or before i and after i.
        blocks = 0
        reach = -1
        for i, x in enumerate(nums):
            reach = max(reach, last[x])
            if reach == i:
                blocks += 1
        return pow(2, blocks - 1, MOD)
