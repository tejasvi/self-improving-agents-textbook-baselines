from typing import List


class Solution:
    def numberOfGoodPartitions(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        last = {}
        for i, x in enumerate(nums):
            last[x] = i
        # count number of blocks: positions where the segment can end
        blocks = 0
        reach = -1
        for i, x in enumerate(nums):
            if last[x] > reach:
                reach = last[x]
            if reach == i:
                blocks += 1
        return pow(2, blocks - 1, MOD)
