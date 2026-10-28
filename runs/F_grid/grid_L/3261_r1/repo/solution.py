from typing import List


class Solution:
    def minOrAfterOperations(self, nums: List[int], k: int) -> int:
        n = len(nums)
        FULL = (1 << 30) - 1

        def feasible(forbidden: int) -> bool:
            # Partition nums into maximal number of contiguous segments whose
            # AND has no bit in `forbidden`. Merges needed = n - segments.
            segments = 0
            cur = FULL
            for x in nums:
                cur &= x
                if cur & forbidden == 0:
                    segments += 1
                    cur = FULL
            if segments == 0:
                return False
            return n - segments <= k

        forbidden = 0
        for b in range(29, -1, -1):
            candidate = forbidden | (1 << b)
            if feasible(candidate):
                forbidden = candidate
        return FULL & ~forbidden
