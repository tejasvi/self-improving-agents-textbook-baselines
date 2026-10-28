from typing import *


class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        m = len(conflictingPairs)
        # bucket pairs by their larger element hi, storing (lo, index)
        by_hi = [[] for _ in range(n + 1)]
        for i, (x, y) in enumerate(conflictingPairs):
            lo, hi = (x, y) if x < y else (y, x)
            by_hi[hi].append((lo, i))

        # Running top two of lo values over all pairs with hi <= r (distinct pairs).
        v1 = v2 = 0
        i1 = -1
        base = 0
        gain = [0] * m
        for r in range(1, n + 1):
            for lo, i in by_hi[r]:
                if lo > v1:
                    v2 = v1
                    v1 = lo
                    i1 = i
                elif lo > v2:
                    v2 = lo
            # valid left endpoints for right endpoint r: l > v1
            base += r - v1
            if i1 >= 0:
                # removing pair i1 would raise the bound to v2 for this r
                gain[i1] += v1 - v2
        return base + max(gain) if m else base
