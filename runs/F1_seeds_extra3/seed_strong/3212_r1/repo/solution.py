from typing import *


class Solution:
    def numberOfGoodPartitions(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        last = {}
        for i, x in enumerate(nums):
            last[x] = i
        blocks = 0
        end = -1
        for i, x in enumerate(nums):
            if last[x] > end:
                end = last[x]
            if i == end:
                blocks += 1
        return pow(2, blocks - 1, MOD)
