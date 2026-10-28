from typing import *
from collections import defaultdict


class Solution:
    def maximumSum(self, nums: List[int]) -> int:
        n = len(nums)
        # squarefree kernel of each 1-indexed position
        groups = defaultdict(int)
        for i in range(1, n + 1):
            x = i
            d = 2
            while d * d <= x:
                sq = d * d
                while x % sq == 0:
                    x //= sq
                d += 1
            groups[x] += nums[i - 1]
        return max(groups.values()) if groups else 0
