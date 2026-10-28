from typing import *


class Solution:
    def minOrAfterOperations(self, nums: List[int], k: int) -> int:
        n = len(nums)
        FULL = (1 << 30) - 1
        forbidden = 0  # bits that must be absent from the final OR

        def feasible(F: int) -> bool:
            segs = 0
            cur = FULL
            for x in nums:
                cur &= x
                if cur & F == 0:
                    segs += 1
                    cur = FULL
            # leftover tail (if any) is merged into the last closed segment
            if segs == 0:
                return False
            return n - segs <= k

        for b in range(29, -1, -1):
            cand = forbidden | (1 << b)
            if feasible(cand):
                forbidden = cand
        return FULL ^ forbidden
