from typing import List


class Solution:
    def minOrAfterOperations(self, nums: List[int], k: int) -> int:
        n = len(nums)
        FULL = (1 << 30) - 1

        def feasible(forbidden: int) -> bool:
            # Partition nums into segments whose AND avoids `forbidden` bits.
            # Each closed segment of length L costs L-1 ops; a trailing
            # leftover merges into the last segment at 1 op per element,
            # so total ops = n - number_of_segments.
            segs = 0
            cur = FULL
            for x in nums:
                cur &= x
                if cur & forbidden == 0:
                    segs += 1
                    cur = FULL
            if segs == 0:
                return False
            return n - segs <= k

        forbidden = 0
        for b in range(29, -1, -1):
            cand = forbidden | (1 << b)
            if feasible(cand):
                forbidden = cand
        return FULL ^ forbidden
