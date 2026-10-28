from typing import List
from collections import defaultdict


class Solution:
    def maximumSum(self, nums: List[int]) -> int:
        def square_free_part(x: int) -> int:
            # Remove every square factor from x.
            res = 1
            p = 2
            while p * p <= x:
                while x % (p * p) == 0:
                    x //= p * p
                if x % p == 0:
                    res *= p
                    x //= p
                p += 1
            return res * x

        groups = defaultdict(int)
        for i, v in enumerate(nums, start=1):
            groups[square_free_part(i)] += v
        return max(groups.values()) if groups else 0
