from typing import List


class Solution:
    def minOrAfterOperations(self, nums: List[int], k: int) -> int:
        n = len(nums)
        full = (1 << 30) - 1
        need = n - k  # minimum number of segments required

        def feasible(allowed: int) -> bool:
            # Greedily split into maximal segments whose AND is a submask of allowed.
            cuts = 0
            cur = full
            for x in nums:
                cur &= x
                if cur & ~allowed == 0:
                    cuts += 1
                    cur = full
            # Leftover tail merges into the previous segment (AND only shrinks).
            return cuts >= need and cuts > 0

        forbidden = 0
        for b in range(29, -1, -1):
            trial = forbidden | (1 << b)
            if feasible(full ^ trial):
                forbidden = trial
        return full ^ forbidden
