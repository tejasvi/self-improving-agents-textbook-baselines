from typing import *


class Solution:
    def minimumDifference(self, nums: List[int], k: int) -> int:
        best = float('inf')
        # distinct OR values of subarrays ending at the current index
        cur = set()
        for x in nums:
            new = {x}
            for v in cur:
                new.add(v | x)
            cur = new
            for v in cur:
                d = k - v if k >= v else v - k
                if d < best:
                    best = d
            if best == 0:
                return 0
        return best
