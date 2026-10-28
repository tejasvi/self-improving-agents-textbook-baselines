from typing import List


class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        # For each right endpoint r, only pairs (lo, hi) with hi <= r matter;
        # the subarray must start after the largest such lo (m1).
        # Removing the pair that provides m1 lets the bound fall back to m2.
        by_hi = [[] for _ in range(n + 1)]
        for x, y in conflictingPairs:
            lo, hi = (x, y) if x < y else (y, x)
            by_hi[hi].append(lo)

        base = 0
        gain = {}
        m1 = 0  # largest lo
        m2 = 0  # second largest lo (with multiplicity)
        for r in range(1, n + 1):
            for a in by_hi[r]:
                if a > m1:
                    m1, m2 = a, m1
                elif a > m2:
                    m2 = a
            base += r - m1
            if m1 > 0:
                gain[m1] = gain.get(m1, 0) + (m1 - m2)

        best = max(gain.values(), default=0)
        return base + best
