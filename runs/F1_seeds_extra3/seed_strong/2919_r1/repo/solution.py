from typing import *


class Solution:
    def maxIncreasingGroups(self, usageLimits: List[int]) -> int:
        total = 0
        groups = 0
        for x in sorted(usageLimits):
            total += x
            # next group needs groups+1 distinct numbers
            if total >= groups + 1:
                groups += 1
                total -= groups
        return groups
