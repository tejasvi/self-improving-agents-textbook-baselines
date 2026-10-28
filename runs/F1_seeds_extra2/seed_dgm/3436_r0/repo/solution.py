from typing import List


class Solution:
    def minimumDifference(self, nums: List[int], k: int) -> int:
        best = float("inf")
        # Distinct OR values of subarrays ending at the current index.
        ors = set()
        for x in nums:
            ors = {v | x for v in ors}
            ors.add(x)
            for v in ors:
                d = abs(k - v)
                if d < best:
                    best = d
            if best == 0:
                return 0
        return best
