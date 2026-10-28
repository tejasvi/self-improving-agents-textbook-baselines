from typing import List


class Solution:
    def minimumDifference(self, nums: List[int], k: int) -> int:
        best = float("inf")
        # Distinct OR values of subarrays ending at the current index.
        # OR values only gain bits as subarrays grow, so this set has
        # at most ~31 distinct values (bounded by bit-width).
        ors = set()
        for x in nums:
            new = {x}
            for v in ors:
                new.add(v | x)
            ors = new
            for v in ors:
                d = abs(v - k)
                if d < best:
                    best = d
            if best == 0:
                return 0
        return int(best)
