from typing import List


class Solution:
    def minimumOperations(self, nums: List[int], target: List[int]) -> int:
        # f = target - nums, padded with zeros on both sides.
        # Each range +-1 operation changes exactly two adjacent differences
        # by +-1 each, so the answer is half the total absolute jump.
        prev = 0
        total = 0
        for a, b in zip(nums, target):
            cur = b - a
            total += abs(cur - prev)
            prev = cur
        total += abs(prev)
        return total // 2
