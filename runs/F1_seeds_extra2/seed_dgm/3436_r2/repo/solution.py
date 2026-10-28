from typing import List


class Solution:
    def minimumDifference(self, nums: List[int], k: int) -> int:
        best = float('inf')
        # Distinct OR values of subarrays ending at the current index.
        cur = set()
        for x in nums:
            cur = {v | x for v in cur}
            cur.add(x)
            for v in cur:
                d = abs(v - k)
                if d < best:
                    best = d
            if best == 0:
                break
        return int(best)
