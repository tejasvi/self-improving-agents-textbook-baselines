from typing import List

class Solution:
    def maxIncreasingGroups(self, usageLimits: List[int]) -> int:
        """Return the maximum number of groups with strictly increasing lengths.

        We can think of forming groups with lengths 1, 2, 3, ... , g.
        each number i can appear in at most usageLimits[i] groups, and a group
        cannot contain duplicate numbers.
        Sorting the limits and greedily trying to extend the current group size
        yields the optimal answer (LeetCode 2352).
        """
        usageLimits.sort()
        cur = 0  # current length we are able to achieve using processed numbers
        ans = 0
        for limit in usageLimits:
            # we can either start a new longer group (cur+1) or are constrained by limit
            cur = min(cur + 1, limit)
            if cur > ans:
                ans = cur
        return ans
