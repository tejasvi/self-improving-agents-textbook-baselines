from typing import *


class Solution:
    def minOrAfterOperations(self, nums: List[int], k: int) -> int:
        FULL = (1 << 30) - 1

        def feasible(allowed: int) -> bool:
            # Greedy: close a segment as soon as its AND is a submask of
            # `allowed`; every element that does not close a segment costs
            # one merge operation.
            ops = 0
            cur = FULL
            notallowed = ~allowed
            for x in nums:
                cur &= x
                if cur & notallowed == 0:
                    cur = FULL
                else:
                    ops += 1
                    if ops > k:
                        return False
            return True

        # Try clearing bits from the highest to the lowest.
        allowed = FULL
        for bit in range(29, -1, -1):
            cand = allowed & ~(1 << bit)
            if feasible(cand):
                allowed = cand
        return allowed
