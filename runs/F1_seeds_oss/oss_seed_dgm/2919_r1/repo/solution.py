from typing import List

class Solution:
    def maxIncreasingGroups(self, usageLimits: List[int]) -> int:
        """Return the maximum number of groups with strictly increasing lengths.
        
        We sort the usage limits so we consider numbers with fewer available
        usages first. While iterating, we maintain `cur`, the total number of
        remaining usages from numbers processed so far. A new group of size
        `k` (where `k = groups + 1`) can be formed if `cur` has at least `k`
        spare usages, because we can pick `k` distinct numbers each contributing
        one usage to the group. After forming such a group we consume `k`
        usages, so we subtract `k` from `cur` and increment `groups`.
        
        It is possible to form several groups after adding a new limit, so we
        repeat the check in a while‑loop.
        """
        usageLimits.sort()
        groups = 0  # number of groups formed so far
        cur = 0     # total spare usages from processed numbers
        for limit in usageLimits:
            cur += limit
            # Try to create as many new groups as possible.
            while cur >= groups + 1:
                groups += 1
                cur -= groups
        return groups
