from typing import List


class Solution:
    def minimumDifference(self, nums: List[int], k: int) -> int:
        best = float("inf")
        cur = set()  # distinct OR values of subarrays ending at previous index
        for x in nums:
            nxt = {x}
            for v in cur:
                nxt.add(v | x)
            cur = nxt
            for v in cur:
                d = abs(k - v)
                if d < best:
                    best = d
            if best == 0:
                break
        return best
