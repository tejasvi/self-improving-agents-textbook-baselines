from typing import List


class Solution:
    def minOrAfterOperations(self, nums: List[int], k: int) -> int:
        n = len(nums)
        FULL = (1 << 30) - 1

        def feasible(allowed: int) -> bool:
            forbidden = FULL & ~allowed
            segs = 0
            cur = FULL
            for x in nums:
                cur &= x
                if cur & forbidden == 0:
                    segs += 1
                    cur = FULL
            # Unclosed tail (if any) is merged into the last closed segment.
            if segs == 0:
                return False
            return n - segs <= k

        ans = FULL
        for b in range(29, -1, -1):
            cand = ans & ~(1 << b)
            if feasible(cand):
                ans = cand
        return ans
