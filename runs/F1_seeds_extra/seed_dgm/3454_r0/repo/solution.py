from typing import List


class Solution:
    def minimumOperations(self, nums: List[int], target: List[int]) -> int:
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
        # final transition back to 0
        diff = -prev
        if diff > 0:
            pos += diff
        else:
            neg -= diff
        return max(pos, neg)
