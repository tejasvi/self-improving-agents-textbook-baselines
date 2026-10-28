from typing import List


class Solution:
    def minimumOperations(self, nums: List[int], target: List[int]) -> int:
        pos = 0
        neg = 0
        prev = 0
        for a, b in zip(nums, target):
            d = b - a
            e = d - prev
            if e > 0:
                pos += e
            else:
                neg -= e
            prev = d
        return max(pos, neg)
