from typing import *


class Solution:
    def numberOfGoodPartitions(self, nums: List[int]) -> int:
        MOD = 10 ** 9 + 7
        last = {}
        for i, x in enumerate(nums):
            last[x] = i
        blocks = 0
        reach = -1
        for i, x in enumerate(nums):
            if i > reach:
                blocks += 1
            reach = max(reach, last[x])
        return pow(2, blocks - 1, MOD)
