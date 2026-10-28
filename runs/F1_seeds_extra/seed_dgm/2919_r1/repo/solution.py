from typing import List


class Solution:
    def maxIncreasingGroups(self, usageLimits: List[int]) -> int:
        # Groups must have sizes 1, 2, ..., k at minimum; greedily build them
        # from the smallest usage limits upward.
        total = 0
        groups = 0
        for x in sorted(usageLimits):
            total += x
            # Need total >= sum of sizes 1..(groups+1) to open another group.
            need = (groups + 1) * (groups + 2) // 2
            if total >= need:
                groups += 1
        return groups
