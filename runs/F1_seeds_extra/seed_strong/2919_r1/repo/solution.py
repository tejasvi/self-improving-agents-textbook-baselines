from typing import *


class Solution:
    def maxIncreasingGroups(self, usageLimits: List[int]) -> int:
        # Greedily build groups of size 1, 2, 3, ... using the smallest limits first.
        total = 0
        groups = 0
        for x in sorted(usageLimits):
            total += x
            if total >= groups + 1:
                groups += 1
                total -= groups
        return groups
