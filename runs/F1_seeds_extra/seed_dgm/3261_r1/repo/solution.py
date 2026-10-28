from typing import List


class Solution:
    def minOrAfterOperations(self, nums: List[int], k: int) -> int:
        n = len(nums)
        full = (1 << 30) - 1
        zero_mask = 0  # bits that must be zero in the final OR

        def feasible(z: int) -> bool:
            segments = 0
            cur = full
            for x in nums:
                cur &= x
                if cur & z == 0:
                    segments += 1
                    cur = full
            if segments == 0:
                return False
            return n - segments <= k

        for b in range(29, -1, -1):
            cand = zero_mask | (1 << b)
            if feasible(cand):
                zero_mask = cand

        return full & ~zero_mask
