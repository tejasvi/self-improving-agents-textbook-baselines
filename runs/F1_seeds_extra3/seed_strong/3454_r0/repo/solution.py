from typing import *


class Solution:
    def minimumOperations(self, nums: List[int], target: List[int]) -> int:
        # d[i] = target[i] - nums[i]; each operation adds +1 at one jump and -1 at another,
        # so the answer is the sum of positive jumps of d, padded with 0 on both ends.
        prev = 0
        total = 0
        for a, b in zip(nums, target):
            cur = b - a
            if cur > prev:
                total += cur - prev
            prev = cur
        # final jump from prev back to the padding 0
        if prev < 0:
            total += -prev
        return total
