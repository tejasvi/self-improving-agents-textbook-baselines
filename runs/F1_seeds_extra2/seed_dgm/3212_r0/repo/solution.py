from typing import List


class Solution:
    def numberOfGoodPartitions(self, nums: List[int]) -> int:
        MOD = 10 ** 9 + 7
        last = {}
        for i, v in enumerate(nums):
            last[v] = i
        blocks = 0
        reach = 0
        for i, v in enumerate(nums):
            reach = max(reach, last[v])
            if i == reach:
                blocks += 1
        return pow(2, blocks - 1, MOD)
