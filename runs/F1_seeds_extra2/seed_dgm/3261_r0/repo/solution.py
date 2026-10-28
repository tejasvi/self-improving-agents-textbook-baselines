from typing import List


class Solution:
    def minOrAfterOperations(self, nums: List[int], k: int) -> int:
        n = len(nums)
        full = (1 << 30) - 1

        def feasible(allowed: int) -> bool:
            # Partition nums into maximal segments whose AND is a subset of `allowed`.
            # Cost of a segment of length L is L-1 operations; total cost = n - segments.
            need = n - k  # minimum number of resulting elements
            segs = 0
            cur = full
            for x in nums:
                cur &= x
                if cur & ~allowed == 0:
                    segs += 1
                    cur = full
            # Any unclosed tail merges into the last closed segment (still valid).
            return segs >= max(need, 1)

        ans = full
        for b in range(29, -1, -1):
            cand = ans & ~(1 << b)
            if feasible(cand):
                ans = cand
        return ans
