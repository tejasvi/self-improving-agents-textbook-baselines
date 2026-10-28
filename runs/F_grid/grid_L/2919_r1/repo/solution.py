from typing import List


class Solution:
    def maxIncreasingGroups(self, usageLimits: List[int]) -> int:
        # Sort ascending; greedily form groups of size 1, 2, 3, ...
        # total = sum of usages available so far minus those already consumed.
        total = 0
        groups = 0
        for x in sorted(usageLimits):
            total += x
            # Next group must have size groups + 1 and needs distinct numbers.
            if total >= groups + 1:
                groups += 1
                total -= groups
        return groups
