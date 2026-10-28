from typing import List


class Solution:
    def minOrAfterOperations(self, nums: List[int], k: int) -> int:
        FULL = (1 << 30) - 1

        def feasible(allowed: int) -> bool:
            # Partition nums into contiguous segments whose AND is a submask
            # of `allowed`. A segment of length L costs L - 1 operations, so
            # total cost = n - (number of segments). Greedily close segments
            # as early as possible to maximize the segment count. A leftover
            # tail can be folded into the last closed segment (its AND only
            # shrinks, so it stays a submask of `allowed`).
            segs = 0
            cur = FULL
            for x in nums:
                cur &= x
                if cur & ~allowed == 0:
                    segs += 1
                    cur = FULL
            if segs == 0:
                return False
            return len(nums) - segs <= k

        allowed = FULL
        for b in range(29, -1, -1):
            cand = allowed & ~(1 << b)
            if feasible(cand):
                allowed = cand
        return allowed
