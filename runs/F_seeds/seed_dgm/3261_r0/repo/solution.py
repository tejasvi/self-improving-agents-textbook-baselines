from typing import List


class Solution:
    def minOrAfterOperations(self, nums: List[int], k: int) -> int:
        n = len(nums)
        FULL = (1 << 30) - 1

        def feasible(forbidden: int) -> bool:
            # Partition nums into consecutive segments whose AND has no forbidden bit.
            # A segment of length L costs L-1 operations. Leftover trailing elements
            # are merged into the last completed segment (each costs one operation).
            groups = 0
            cur = FULL
            length = 0
            ops = 0
            for x in nums:
                cur &= x
                length += 1
                if cur & forbidden == 0:
                    ops += length - 1
                    groups += 1
                    cur = FULL
                    length = 0
            if length > 0:
                if groups == 0:
                    return False
                ops += length
            return ops <= k

        ans = 0
        for bit in range(29, -1, -1):
            cand = ans | (1 << bit)
            if feasible(cand):
                ans = cand
        return FULL ^ ans
