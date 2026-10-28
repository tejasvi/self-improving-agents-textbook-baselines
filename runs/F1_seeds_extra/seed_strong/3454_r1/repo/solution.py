from typing import *


class Solution:
    def minimumOperations(self, nums: List[int], target: List[int]) -> int:
        pos = 0
        neg = 0
        prev = 0
        for a, b in zip(nums, target):
            d = b - a
            diff = d - prev
            if diff > 0:
                pos += diff
            else:
                neg -= diff
            prev = d
        # final boundary: d_n = 0
        diff = -prev
        if diff > 0:
            pos += diff
        else:
            neg -= diff
        return max(pos, neg)
