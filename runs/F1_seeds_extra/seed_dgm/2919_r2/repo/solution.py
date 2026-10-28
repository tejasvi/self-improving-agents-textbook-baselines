from typing import List


class Solution:
    def maxIncreasingGroups(self, usageLimits: List[int]) -> int:
        # Greedy: process limits in ascending order, accumulating available uses.
        # Whenever the pool can fill a group of size ans+1, form it.
        # Each group must be strictly larger than the previous one, so
        # the groups are sized 1, 2, 3, ... and the pool carries leftovers forward.
        usageLimits.sort()
        ans = 0
        total = 0
        for x in usageLimits:
            total += x
            if total > ans:
                ans += 1
                total -= ans
        return ans
