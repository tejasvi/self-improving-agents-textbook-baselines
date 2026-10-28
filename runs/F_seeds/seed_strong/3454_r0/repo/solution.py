from typing import *


class Solution:
    def minimumOperations(self, nums: List[int], target: List[int]) -> int:
        # d[i] = target[i] - nums[i]; each op is a range +/-1 on d.
        # Minimum ops = max(sum of positive jumps, sum of negative jumps)
        # of d padded with a leading 0.
        pos = 0
        neg = 0
        prev = 0
        for a, b in zip(nums, target):
            cur = b - a
            diff = cur - prev
            if diff > 0:
                pos += diff
            else:
                neg -= diff
            prev = cur
        return max(pos, neg)
