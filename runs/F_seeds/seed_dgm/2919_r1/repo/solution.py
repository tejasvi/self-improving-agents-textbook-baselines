from typing import List


class Solution:
    def maxIncreasingGroups(self, usageLimits: List[int]) -> int:
        total = 0
        k = 0
        for x in sorted(usageLimits):
            total += x
            if total >= k + 1:
                k += 1
                total -= k
        return k
