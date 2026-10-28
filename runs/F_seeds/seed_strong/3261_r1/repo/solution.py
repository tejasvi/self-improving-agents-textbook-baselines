from typing import *


class Solution:
    def minOrAfterOperations(self, nums: List[int], k: int) -> int:
        FULL = (1 << 30) - 1

        def feasible(allowed: int) -> bool:
            # Greedily close segments as soon as their AND fits in `allowed`.
            ops = 0
            cur = FULL
            length = 0
            groups = 0
            notallowed = FULL & ~allowed
            for x in nums:
                cur &= x
                length += 1
                if cur & notallowed == 0:
                    ops += length - 1
                    groups += 1
                    cur = FULL
                    length = 0
            if length > 0:
                if groups == 0:
                    return False
                # leftover elements merge into the last closed group
                ops += length
            return ops <= k

        ans = FULL
        for b in range(29, -1, -1):
            cand = ans ^ (1 << b)
            if feasible(cand):
                ans = cand
        return ans
