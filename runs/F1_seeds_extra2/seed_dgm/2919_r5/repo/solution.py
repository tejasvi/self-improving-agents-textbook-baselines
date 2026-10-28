from typing import List


class Solution:
    def maxIncreasingGroups(self, usageLimits: List[int]) -> int:
        # Greedy: process limits in ascending order, accumulating available
        # usage. Whenever we have enough to fill a group of size k+1 (the
        # next group must be strictly longer than the previous ones), form it.
        s = 0
        k = 0
        for u in sorted(usageLimits):
            s += u
            if s >= k + 1:
                k += 1
                s -= k
        return k
