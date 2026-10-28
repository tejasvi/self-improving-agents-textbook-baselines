from typing import *
from collections import defaultdict


class Solution:
    def maximumSum(self, nums: List[int]) -> int:
        n = len(nums)
        groups = defaultdict(int)
        for i, v in enumerate(nums):
            k = i + 1
            sf = k
            p = 2
            while p * p <= k:
                q = p * p
                while sf % q == 0:
                    sf //= q
                p += 1
            groups[sf] += v
        return max(groups.values()) if groups else 0
