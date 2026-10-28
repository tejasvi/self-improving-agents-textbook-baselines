from typing import List


class Solution:
    def minimumOperations(self, nums: List[int], target: List[int]) -> int:
        # d[i] = target[i] - nums[i]; the difference array of d (padded with 0
        # at both ends) must be zeroed. Each operation changes two entries of
        # this array by +1 and -1, so it reduces the total absolute value by at
        # most 2. The answer is sum(|e|) / 2.
        prev = 0
        total = 0
        for a, b in zip(nums, target):
            cur = b - a
            total += abs(cur - prev)
            prev = cur
        total += abs(prev)
        return total // 2
