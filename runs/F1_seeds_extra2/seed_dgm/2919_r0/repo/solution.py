from typing import List


class Solution:
    def maxIncreasingGroups(self, usageLimits: List[int]) -> int:
        # Greedy: process limits in ascending order, building groups of
        # size 1, 2, 3, ... Each group of size k+1 needs k+1 distinct
        # numbers; leftover usage slots carry over to later groups.
        carry = 0
        groups = 0
        for u in sorted(usageLimits):
            carry += u
            if carry >= groups + 1:
                groups += 1
                carry -= groups
        return groups
