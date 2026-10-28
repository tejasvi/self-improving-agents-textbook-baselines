from typing import *


class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        # Group pairs by their larger element (right endpoint).
        by_hi = [[] for _ in range(n + 1)]
        for idx, (a, b) in enumerate(conflictingPairs):
            lo, hi = (a, b) if a < b else (b, a)
            by_hi[hi].append((lo, idx))

        m = len(conflictingPairs)
        extra = [0] * m
        base = 0
        max1 = 0      # largest lo among pairs seen so far
        max1_idx = -1
        max2 = 0      # second largest lo (from a different pair)
        for r in range(1, n + 1):
            for lo, idx in by_hi[r]:
                if lo > max1:
                    max2 = max1
                    max1 = lo
                    max1_idx = idx
                elif lo > max2:
                    max2 = lo
            base += r - max1
            if max1 > 0:
                extra[max1_idx] += max1 - max2
        return base + max(extra)
