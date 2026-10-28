from typing import List


class Solution:
    def minOrAfterOperations(self, nums: List[int], k: int) -> int:
        n = len(nums)
        full = (1 << 30) - 1

        def feasible(forbidden: int) -> bool:
            groups = 0
            cur = full
            for x in nums:
                cur &= x
                if cur & forbidden == 0:
                    groups += 1
                    cur = full
            if groups == 0:
                return False
            # leftover tail (if any) is absorbed into the last group
            return n - groups <= k

        forbidden = 0
        for bit in range(29, -1, -1):
            candidate = forbidden | (1 << bit)
            if feasible(candidate):
                forbidden = candidate
        return full ^ forbidden
