from typing import *


class Solution:
    def maxIncreasingGroups(self, usageLimits: List[int]) -> int:
        k = 0
        s = 0
        for x in sorted(usageLimits):
            s += x
            if s >= k + 1:
                k += 1
                s -= k
        return k
