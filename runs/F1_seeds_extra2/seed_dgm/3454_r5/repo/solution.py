from typing import List


class Solution:
    def minimumOperations(self, nums: List[int], target: List[int]) -> int:
        # d[i] = target[i] - nums[i]; the answer is half the total variation
        # of d padded with zeros on both ends.
        total = 0
        prev = 0
        for a, b in zip(nums, target):
            cur = b - a
            total += abs(cur - prev)
            prev = cur
        total += abs(prev)  # transition back to 0 at the end
        return total // 2
