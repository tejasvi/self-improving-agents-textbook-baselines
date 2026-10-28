from typing import List


class Solution:
    def minimumOperations(self, nums: List[int], target: List[int]) -> int:
        # d[i] = target[i] - nums[i], padded with 0 on both ends.
        # Each operation changes the difference array at two positions by
        # opposite amounts, so it reduces sum|D| by at most 2; this is achievable.
        total = 0
        prev = 0
        for a, b in zip(nums, target):
            d = b - a
            total += abs(d - prev)
            prev = d
        total += abs(prev)  # close with d[n] = 0
        return total // 2
