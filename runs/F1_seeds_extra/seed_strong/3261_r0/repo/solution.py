from typing import *


class Solution:
    def minOrAfterOperations(self, nums: List[int], k: int) -> int:
        n = len(nums)
        FULL = (1 << 30) - 1

        def feasible(mask: int) -> bool:
            # Greedily split into the maximum number of segments whose AND
            # is a submask of mask. Operations used = n - segments.
            need = n - k
            segs = 0
            cur = FULL
            for x in nums:
                cur &= x
                if cur & ~mask == 0:
                    segs += 1
                    cur = FULL
                    if segs >= need:
                        return True
            # Leftover elements (cur not reset) merge into the last segment,
            # whose AND only shrinks, so it stays valid.
            return segs >= need and segs > 0

        ans = FULL
        for b in range(29, -1, -1):
            t = ans ^ (1 << b)
            if feasible(t):
                ans = t
        return ans
