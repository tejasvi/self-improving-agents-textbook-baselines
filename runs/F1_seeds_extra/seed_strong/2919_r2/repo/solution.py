from typing import *


class Solution:
    def maxIncreasingGroups(self, usageLimits: List[int]) -> int:
        cur = 0
        ans = 0
        for x in sorted(usageLimits):
            cur += x
            if cur >= ans + 1:
                ans += 1
                cur -= ans
        return ans
