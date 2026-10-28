from typing import List


class Solution:
    def minimumOperations(self, nums: List[int], target: List[int]) -> int:
        # d[i] = target[i] - nums[i]; answer = sum(|d[i] - d[i-1]|) over
        # i in 0..n with d[-1] = d[n] = 0, divided by 2.
        prev = 0
        total = 0
        for a, b in zip(nums, target):
            cur = b - a
            total += abs(cur - prev)
            prev = cur
        total += abs(prev)
        return total // 2
