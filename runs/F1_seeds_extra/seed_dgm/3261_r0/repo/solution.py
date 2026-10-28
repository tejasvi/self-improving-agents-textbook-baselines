from typing import List


class Solution:
    def minOrAfterOperations(self, nums: List[int], k: int) -> int:
        n = len(nums)
        full = (1 << 30) - 1

        def feasible(Z: int) -> bool:
            # Count maximal number of disjoint contiguous segments whose AND
            # has no bits in Z. Merges needed = n - segments.
            segments = 0
            cur = full
            for x in nums:
                cur &= x
                if cur & Z == 0:
                    segments += 1
                    cur = full
            if segments == 0:
                return False
            return n - segments <= k

        Z = 0
        for bit in range(29, -1, -1):
            cand = Z | (1 << bit)
            if feasible(cand):
                Z = cand
        return full & ~Z
