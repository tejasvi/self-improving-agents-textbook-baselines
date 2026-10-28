from typing import List
from collections import defaultdict


class Solution:
    def maximumSum(self, nums: List[int]) -> int:
        def square_free_part(x: int) -> int:
            res = 1
            d = 2
            while d * d <= x:
                while x % (d * d) == 0:
                    x //= d * d
                if x % d == 0:
                    res *= d
                    x //= d
                d += 1
            return res * x

        groups = defaultdict(int)
        for i, v in enumerate(nums, start=1):
            groups[square_free_part(i)] += v
        return max(groups.values()) if groups else 0
