from typing import List


class Solution:
    def maxIncreasingGroups(self, usageLimits: List[int]) -> int:
        # Greedy: sort ascending; accumulate available usages. Whenever the pool
        # can supply a group of size groups+1, form it (sizes strictly increase).
        groups = 0
        pool = 0
        for u in sorted(usageLimits):
            pool += u
            if pool >= groups + 1:
                groups += 1
                pool -= groups
        return groups
