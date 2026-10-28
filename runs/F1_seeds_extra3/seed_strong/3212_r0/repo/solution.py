from typing import *


class Solution:
    def numberOfGoodPartitions(self, nums: List[int]) -> int:
        MOD = 10 ** 9 + 7
        last = {}
        for i, v in enumerate(nums):
            last[v] = i
        blocks = 0
        reach = -1
        for i, v in enumerate(nums):
            if last[v] > reach:
                reach = last[v]
            if reach == i:
                blocks += 1
        return pow(2, blocks - 1, MOD)
