from typing import List


class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        m = len(conflictingPairs)
        # Group pairs by their larger endpoint.
        by_hi = [[] for _ in range(n + 1)]
        for idx, (a, b) in enumerate(conflictingPairs):
            lo, hi = min(a, b), max(a, b)
            by_hi[hi].append((lo, idx))

        gain = [0] * m
        base = 0
        # Top two left bounds (value, index) among pairs with hi <= r.
        v1, i1 = 0, -1
        v2 = 0
        for r in range(1, n + 1):
            for lo, idx in by_hi[r]:
                if lo > v1:
                    v2 = v1
                    v1, i1 = lo, idx
                elif lo > v2:
                    v2 = lo
            # Subarrays ending at r that are valid with all pairs present.
            base += r - v1
            if i1 >= 0:
                gain[i1] += v1 - v2

        return base + (max(gain) if m else 0)
