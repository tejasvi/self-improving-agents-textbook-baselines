from typing import *


class Solution:
    def minOrAfterOperations(self, nums: List[int], k: int) -> int:
        n = len(nums)

        def feasible(X: int) -> bool:
            # Partition into maximal segments whose AND is a submask of X.
            # Leftover tail is merged into the last completed segment.
            segments = 0
            cur = -1  # all bits set
            for x in nums:
                cur &= x
                if cur & ~X == 0:
                    segments += 1
                    cur = -1
            if segments == 0:
                return False
            return n - segments <= k

        X = (1 << 30) - 1
        for b in range(29, -1, -1):
            cand = X ^ (1 << b)
            if feasible(cand):
                X = cand
        return X
