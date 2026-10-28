from typing import *


class Solution:
    def minimumOperations(self, nums: List[int], target: List[int]) -> int:
        total = 0
        prev = 0
        for a, b in zip(nums, target):
            d = b - a
            total += abs(d - prev)
            prev = d
        total += abs(prev)
        return total // 2
