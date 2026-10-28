from typing import *


class Solution:
    def minOrAfterOperations(self, nums: List[int], k: int) -> int:
        n = len(nums)
        full = (1 << 30) - 1

        def feasible(mask: int) -> bool:
            # Greedily split into max number of segments whose AND is a submask of mask.
            # Each segment of length L costs L-1 operations; total cost = n - segments.
            segs = 0
            cur = full
            inv = ~mask
            for x in nums:
                cur &= x
                if cur & inv == 0:
                    segs += 1
                    cur = full
            return segs > 0 and n - segs <= k

        mask = full
        for b in range(29, -1, -1):
            cand = mask & ~(1 << b)
            if feasible(cand):
                mask = cand
        return mask
