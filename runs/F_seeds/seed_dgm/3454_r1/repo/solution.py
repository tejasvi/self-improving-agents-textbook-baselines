from typing import List


class Solution:
    def minimumOperations(self, nums: List[int], target: List[int]) -> int:
        # d[i] = target[i] - nums[i]; pad with 0 on both sides and
        # take the difference array. Each operation changes two entries
        # of the difference array by +1 and -1, so the answer is half the
        # total absolute difference.
        prev = 0
        total = 0
        for a, b in zip(nums, target):
            cur = b - a
            total += abs(cur - prev)
            prev = cur
        total += abs(prev)
        return total // 2
