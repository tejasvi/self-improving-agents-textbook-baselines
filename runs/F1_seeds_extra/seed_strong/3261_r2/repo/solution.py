from typing import *


class Solution:
    def minOrAfterOperations(self, nums: List[int], k: int) -> int:
        FULL = (1 << 30) - 1
        n = len(nums)

        def feasible(allowed: int) -> bool:
            # Partition into contiguous segments whose AND is a subset of `allowed`,
            # using the maximum number of segments; ops = n - segments.
            ops = 0
            segs = 0
            cur = FULL
            length = 0
            for x in nums:
                cur &= x
                length += 1
                if cur & ~allowed == 0:
                    ops += length - 1
                    segs += 1
                    cur = FULL
                    length = 0
            if length > 0:
                if segs == 0:
                    return False
                # merge leftover elements into the last closed segment
                ops += length
            return ops <= k

        forbidden = 0
        for b in range(29, -1, -1):
            cand = forbidden | (1 << b)
            if feasible(FULL & ~cand):
                forbidden = cand
        return FULL & ~forbidden
