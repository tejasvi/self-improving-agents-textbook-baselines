from typing import List


class Solution:
    def minimumDifference(self, nums: List[int], k: int) -> int:
        best = float("inf")
        ors = []  # distinct OR values of subarrays ending at the current index
        for x in nums:
            new = {x}
            for v in ors:
                new.add(v | x)
            ors = list(new)
            for v in ors:
                d = abs(k - v)
                if d < best:
                    best = d
            if best == 0:
                break
        return best
