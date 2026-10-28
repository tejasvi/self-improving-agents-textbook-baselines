from typing import List


class Solution:
    def maxIncreasingGroups(self, usageLimits: List[int]) -> int:
        # Greedy: process limits in ascending order, accumulating available usages.
        # Groups have sizes 1, 2, ..., k at minimum; open group k+1 once the
        # accumulated usage covers it.
        total = 0
        groups = 0
        for x in sorted(usageLimits):
            total += x
            if total >= groups + 1:
                groups += 1
                total -= groups
        return groups
