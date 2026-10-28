from typing import *


class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        m = len(conflictingPairs)
        # For each right endpoint r, the pairs with that right endpoint.
        by_r = [[] for _ in range(n + 1)]
        for idx, (a, b) in enumerate(conflictingPairs):
            l, r = (a, b) if a < b else (b, a)
            by_r[r].append((l, idx))
        b1 = 0          # largest left endpoint among pairs with r' <= R
        b2 = 0          # second largest (from a different pair)
        best_idx = -1   # index of pair achieving b1
        base = 0
        gain = [0] * m
        for R in range(1, n + 1):
            for l, idx in by_r[R]:
                if l > b1:
                    b2 = b1
                    b1 = l
                    best_idx = idx
                elif l > b2:
                    b2 = l
            base += R - b1
            if best_idx >= 0:
                gain[best_idx] += b1 - b2
        return base + max(gain)
