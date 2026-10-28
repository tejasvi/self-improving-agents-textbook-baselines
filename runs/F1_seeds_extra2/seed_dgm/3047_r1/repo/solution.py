from typing import List
from collections import defaultdict


class Solution:
    def maximumSum(self, nums: List[int]) -> int:
        def square_free_part(x: int) -> int:
            res = 1
            p = 2
            while p * p <= x:
                cnt = 0
                while x % p == 0:
                    x //= p
                    cnt ^= 1
                if cnt:
                    res *= p
                p += 1
            return res * x

        groups = defaultdict(int)
        for i, v in enumerate(nums, start=1):
            groups[square_free_part(i)] += v
        return max(groups.values())
