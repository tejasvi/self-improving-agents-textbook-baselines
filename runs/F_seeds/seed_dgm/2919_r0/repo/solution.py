from typing import List


class Solution:
    def maxIncreasingGroups(self, usageLimits: List[int]) -> int:
        # Greedily form groups of sizes 1, 2, 3, ... using the smallest limits first.
        # `cur` is the number of usages available (carried over) from the processed prefix.
        usageLimits.sort()
        groups = 0
        cur = 0
        for x in usageLimits:
            cur += x
            if cur >= groups + 1:
                groups += 1
                cur -= groups
        return groups
