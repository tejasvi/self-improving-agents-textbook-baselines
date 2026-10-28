from typing import List


class Solution:
    def maxIncreasingGroups(self, usageLimits: List[int]) -> int:
        # Sort ascending; greedily form groups of size 1, 2, 3, ...
        # `pool` holds usages available (carried over) but not yet placed.
        groups = 0
        pool = 0
        for x in sorted(usageLimits):
            pool += x
            # Next group needs groups+1 distinct numbers.
            if pool >= groups + 1:
                groups += 1
                pool -= groups
        return groups
