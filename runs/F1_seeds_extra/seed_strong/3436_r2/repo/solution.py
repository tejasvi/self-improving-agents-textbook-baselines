from typing import *


class Solution:
    def minimumDifference(self, nums: List[int], k: int) -> int:
        best = abs(k - nums[0])
        cur = set()  # distinct ORs of subarrays ending at previous index
        for x in nums:
            nxt = {x}
            for v in cur:
                nxt.add(v | x)
            cur = nxt
            for v in cur:
                d = k - v if k >= v else v - k
                if d < best:
                    best = d
        return best
