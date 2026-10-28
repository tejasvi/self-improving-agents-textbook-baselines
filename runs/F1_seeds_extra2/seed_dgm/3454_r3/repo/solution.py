from typing import List


class Solution:
    def minimumOperations(self, nums: List[int], target: List[int]) -> int:
        # d = target - nums; answer = sum of positive parts of the
        # difference array of d (padded with zeros on both sides).
        prev = 0
        total = 0
        for a, b in zip(nums, target):
            cur = b - a
            diff = cur - prev
            if diff > 0:
                total += diff
            prev = cur
        # final boundary: 0 - prev
        if -prev > 0:
            total += -prev
        return total
