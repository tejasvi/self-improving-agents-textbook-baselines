from typing import List


class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        m = len(conflictingPairs)
        # Group pairs by their larger endpoint.
        by_max = [[] for _ in range(n + 1)]
        for idx, (a, b) in enumerate(conflictingPairs):
            lo, hi = (a, b) if a < b else (b, a)
            by_max[hi].append((lo, idx))

        gain = [0] * m
        base = 0
        # Top two left-bounds (value, index) among pairs with max <= r.
        best1 = (0, -1)
        best2 = (0, -1)
        for r in range(1, n + 1):
            for lo, idx in by_max[r]:
                if lo > best1[0]:
                    best2 = best1
                    best1 = (lo, idx)
                elif lo > best2[0]:
                    best2 = (lo, idx)
            base += r - best1[0]
            if best1[1] >= 0:
                gain[best1[1]] += best1[0] - best2[0]

        return base + max(gain)
