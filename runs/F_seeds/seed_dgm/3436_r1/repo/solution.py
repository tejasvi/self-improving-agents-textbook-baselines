from typing import List


class Solution:
    def minimumDifference(self, nums: List[int], k: int) -> int:
        best = float("inf")
        # distinct OR values of subarrays ending at the current index
        ors = []
        for x in nums:
            new = []
            for v in ors:
                nv = v | x
                if not new or new[-1] != nv:
                    new.append(nv)
            if not new or new[-1] != x:
                new.append(x)
            ors = new
            for v in ors:
                d = abs(k - v)
                if d < best:
                    best = d
                    if best == 0:
                        return 0
        return best
