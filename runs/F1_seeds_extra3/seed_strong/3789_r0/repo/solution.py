from typing import *


class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        by_hi = [[] for _ in range(n + 1)]
        for idx, (a, b) in enumerate(conflictingPairs):
            lo, hi = (a, b) if a < b else (b, a)
            by_hi[hi].append((lo, idx))
        gain = [0] * len(conflictingPairs)
        base = 0
        v1, i1, v2 = 0, -1, 0
        for r in range(1, n + 1):
            for val, idx in by_hi[r]:
                if val > v1:
                    v2 = v1
                    v1, i1 = val, idx
                elif val > v2:
                    v2 = val
            base += r - v1
            if i1 >= 0:
                gain[i1] += v1 - v2
        return base + (max(gain) if gain else 0)
