from typing import List


class Solution:
    def maximumSum(self, nums: List[int]) -> int:
        # i * j is a perfect square iff i and j share the same square-free part.
        groups = {}
        for idx, val in enumerate(nums, start=1):
            # compute square-free part of idx
            sf = 1
            x = idx
            p = 2
            while p * p <= x:
                while x % (p * p) == 0:
                    x //= p * p
                if x % p == 0:
                    sf *= p
                    x //= p
                p += 1
            sf *= x
            groups[sf] = groups.get(sf, 0) + val
        return max(groups.values()) if groups else 0
