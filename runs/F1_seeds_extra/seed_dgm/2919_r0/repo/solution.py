from typing import List


class Solution:
    def maxIncreasingGroups(self, usageLimits: List[int]) -> int:
        # Greedily build groups of sizes 1, 2, 3, ... Each group of size g+1
        # needs g+1 distinct numbers; the accumulated remaining capacity of the
        # smallest-limit numbers seen so far must cover it.
        total = 0
        groups = 0
        for x in sorted(usageLimits):
            total += x
            if total >= groups + 1:
                groups += 1
                total -= groups
        return groups
