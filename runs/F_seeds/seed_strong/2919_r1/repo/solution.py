from typing import *


class Solution:
    def maxIncreasingGroups(self, usageLimits: List[int]) -> int:
        cur = 0
        groups = 0
        need = 1
        for x in sorted(usageLimits):
            cur += x
            if cur >= need:
                cur -= need
                groups += 1
                need += 1
        return groups
