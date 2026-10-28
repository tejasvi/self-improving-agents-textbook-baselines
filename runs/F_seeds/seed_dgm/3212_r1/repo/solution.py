from typing import List


class Solution:
    def numberOfGoodPartitions(self, nums: List[int]) -> int:
        MOD = 10 ** 9 + 7
        n = len(nums)
        last = {}
        for i, x in enumerate(nums):
            last[x] = i
        # count independent blocks: cut after i only if no value spans across i
        blocks = 0
        reach = -1
        for i, x in enumerate(nums):
            reach = max(reach, last[x])
            if reach == i:
                blocks += 1
        return pow(2, blocks - 1, MOD)
