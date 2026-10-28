from typing import List


class Solution:
    def maxIncreasingGroups(self, usageLimits: List[int]) -> int:
        # Greedy: process limits in ascending order, accumulating usable
        # slots. Open the next group (of size groups+1) as soon as the
        # accumulated slots can supply it with distinct numbers.
        groups = 0
        total = 0
        for x in sorted(usageLimits):
            total += x
            if total >= groups + 1:
                groups += 1
                total -= groups
        return groups
