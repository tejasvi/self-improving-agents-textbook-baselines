from typing import List

class Solution:
    def maxIncreasingGroups(self, usageLimits: List[int]) -> int:
        # Sort the usage limits to process smaller limits first.
        usageLimits.sort()
        groups = 0          # Number of groups formed so far
        need = 1            # The required size for the next group
        cur = 0             # Accumulated remaining usage counts
        for limit in usageLimits:
            cur += limit
            # While we have enough accumulated usage to form the next group
            while cur >= need:
                cur -= need
                groups += 1
                need += 1
        return groups
