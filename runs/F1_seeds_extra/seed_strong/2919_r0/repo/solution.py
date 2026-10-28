from typing import *


class Solution:
    def maxIncreasingGroups(self, usageLimits: List[int]) -> int:
        total = 0
        groups = 0
        need = 0  # sum of sizes 1..groups+1 needed to open next group
        for u in sorted(usageLimits):
            total += u
            size = groups + 1
            if total >= need + size:
                groups += 1
                need += size
        return groups
