from typing import *


class Solution:
    def minimumOperations(self, nums: List[int], target: List[int]) -> int:
        # Difference array of d = target - nums, padded with 0 at both ends.
        # Each operation adds +v at l and -v at r+1 (or the reverse), so the
        # minimum number of operations is the sum of positive parts = sum|e|/2.
        prev = 0
        total = 0
        for a, b in zip(nums, target):
            d = b - a
            total += abs(d - prev)
            prev = d
        total += abs(prev)
        return total // 2
