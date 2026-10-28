from typing import List


class Solution:
    def maximumSum(self, nums: List[int]) -> int:
        def square_free_part(x: int) -> int:
            res = x
            d = 2
            while d * d <= x:
                sq = d * d
                while res % sq == 0:
                    res //= sq
                d += 1
            return res

        groups = {}
        for i, v in enumerate(nums, start=1):
            key = square_free_part(i)
            groups[key] = groups.get(key, 0) + v
        return max(groups.values()) if groups else 0
