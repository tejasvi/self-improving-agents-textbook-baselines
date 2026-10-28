from typing import List


class Solution:
    def minOrAfterOperations(self, nums: List[int], k: int) -> int:
        FULL = (1 << 30) - 1

        def feasible(allowed: int) -> bool:
            # Greedily split nums into segments whose AND is a subset of
            # `allowed`, closing each segment as early as possible.
            # A segment of length L costs L-1 operations.
            ops = 0
            segments = 0
            cur = FULL
            length = 0
            for x in nums:
                cur &= x
                length += 1
                if cur & ~allowed == 0:
                    ops += length - 1
                    segments += 1
                    cur = FULL
                    length = 0
            if length > 0:
                # Trailing elements must be merged into the previous segment
                # (AND only shrinks, so the constraint still holds).
                if segments == 0:
                    return False
                ops += length
            return ops <= k

        ans = FULL
        for b in range(29, -1, -1):
            t = ans & ~(1 << b)
            if feasible(t):
                ans = t
        return ans
