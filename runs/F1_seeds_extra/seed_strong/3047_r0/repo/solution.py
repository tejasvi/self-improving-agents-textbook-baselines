from typing import *
from collections import defaultdict


class Solution:
    def maximumSum(self, nums: List[int]) -> int:
        groups = defaultdict(int)
        for i in range(1, len(nums) + 1):
            # square-free part of i
            r = i
            p = 2
            while p * p <= r:
                while r % (p * p) == 0:
                    r //= p * p
                p += 1
            groups[r] += nums[i - 1]
        return max(groups.values()) if groups else 0
