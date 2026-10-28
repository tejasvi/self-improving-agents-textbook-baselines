from typing import *


class Solution:
    def minOrAfterOperations(self, nums: List[int], k: int) -> int:
        n = len(nums)

        def feasible(mask: int) -> bool:
            # Partition nums into maximal segments whose AND is a submask of mask.
            # Cost = n - (#segments); leftover tail merges into the last segment.
            segments = 0
            cur = -1  # all ones
            for x in nums:
                cur &= x
                if cur & ~mask == 0:
                    segments += 1
                    cur = -1
            if segments == 0:
                return False
            return n - segments <= k

        ans = (1 << 30) - 1
        for b in range(29, -1, -1):
            cand = ans & ~(1 << b)
            if feasible(cand):
                ans = cand
        return ans
