from typing import *


class Solution:
    def minimumOperations(self, nums: List[int], target: List[int]) -> int:
        # d = target - nums, padded with 0 on both ends; answer = sum|diff(d)| / 2
        total = 0
        prev = 0
        for a, b in zip(nums, target):
            cur = b - a
            total += abs(cur - prev)
            prev = cur
        total += abs(prev)
        return total // 2
