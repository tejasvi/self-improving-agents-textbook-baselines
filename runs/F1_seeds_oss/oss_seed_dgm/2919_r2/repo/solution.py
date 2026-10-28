"""Solution for LeetCode problem: Maximum Number of Groups With Increasing Length.

Given an array `usageLimits` where `usageLimits[i]` is the maximum number of times
number `i` can appear across all groups, we need to form groups such that:

* Each group contains distinct numbers (no duplicates inside a group).
* The length of each group is strictly larger than the length of the previous one.
* No number is used more than its usage limit.

We must maximise the number of groups.

Observation
------------
If we sort `usageLimits` in non‑decreasing order, we can greedily decide whether a new
group can be created. Suppose we have already managed to build `ans` groups. The next
group must have size `ans + 1`. To obtain a group of that size we need at least one
available usage from `ans + 1` distinct numbers.

When iterating over the sorted limits, each element represents the remaining capacity
of a distinct number. If the current limit is at least `ans + 1`, we can assign one
unit of that number to the new group, thereby increasing `ans` by one. Otherwise the
current number cannot help us form a larger group, and we simply skip it.

Because we process the limits from smallest to largest, the greedy choice is optimal:
using a number with a small limit for a small group leaves the larger limits for
potentially larger groups later on.

The algorithm runs in `O(n log n)` time due to sorting and `O(1)` extra space.
"""

from typing import List


class Solution:
    def maxIncreasingGroups(self, usageLimits: List[int]) -> int:
        """Return the maximum number of groups with strictly increasing lengths.

        Parameters
        ----------
        usageLimits : List[int]
            `usageLimits[i]` is the maximum total times number `i` may be used.

        Returns
        -------
        int
            The largest possible count of groups satisfying the problem conditions.
        """
        # Sort limits to apply the greedy strategy described above.
        usageLimits.sort()
        groups = 0  # number of groups we have successfully built so far
        for limit in usageLimits:
            # To form the next group we need a size of groups + 1.
            if limit >= groups + 1:
                groups += 1
        return groups
