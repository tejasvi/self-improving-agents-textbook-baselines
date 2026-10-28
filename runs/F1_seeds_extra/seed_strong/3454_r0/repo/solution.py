from typing import *


class Solution:
    def minimumOperations(self, nums: List[int], target: List[int]) -> int:
        # d[i] = target[i] - nums[i]; positive and negative parts need
        # opposite operations and are handled independently.
        pos = 0
        neg = 0
        prev_p = 0
        prev_q = 0
        for a, b in zip(nums, target):
            d = b - a
            p = d if d > 0 else 0
            q = -d if d < 0 else 0
            if p > prev_p:
                pos += p - prev_p
            if q > prev_q:
                neg += q - prev_q
            prev_p = p
            prev_q = q
        return pos + neg
