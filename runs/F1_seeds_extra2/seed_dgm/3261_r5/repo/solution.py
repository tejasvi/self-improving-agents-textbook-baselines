from typing import List


class Solution:
    def minOrAfterOperations(self, nums: List[int], k: int) -> int:
        n = len(nums)
        full = (1 << 30) - 1

        def feasible(forbidden: int) -> bool:
            # Greedily split nums into segments whose AND avoids `forbidden` bits.
            # Each segment of length L costs L-1 operations; a leftover tail is
            # merged into the last closed segment (also cost = its length).
            # Total cost = n - segments, which must be <= k, with >= 1 segment.
            segs = 0
            cur = full
            for x in nums:
                cur &= x
                if cur & forbidden == 0:
                    segs += 1
                    cur = full
                    # Reset: next segment starts fresh.
            if segs == 0:
                return False
            return n - segs <= k

        mask = 0
        for b in range(29, -1, -1):
            trial = mask | (1 << b)
            if feasible(trial):
                mask = trial
        return full & ~mask
