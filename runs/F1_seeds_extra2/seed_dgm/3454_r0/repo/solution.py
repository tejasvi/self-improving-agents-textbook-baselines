from typing import List


class Solution:
    def minimumOperations(self, nums: List[int], target: List[int]) -> int:
        # d = target - nums; answer = sum of positive parts of the
        # discrete derivative of d (padded with 0 on both ends).
        prev = 0
        total = 0
        for a, b in zip(nums, target):
            cur = b - a
            diff = cur - prev
            if diff > 0:
                total += diff
            prev = cur
        # Final padding: transition from prev back to 0 (only negative, no cost
        # added to positive sum).
        return total
