from typing import List


class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        m = len(conflictingPairs)
        # group pairs by their larger element (right endpoint)
        by_hi = [[] for _ in range(n + 1)]
        for idx, (x, y) in enumerate(conflictingPairs):
            lo, hi = (x, y) if x < y else (y, x)
            by_hi[hi].append((lo, idx))

        b1, b2, id1 = 0, 0, -1
        base = 0
        bonus = [0] * m
        for r in range(1, n + 1):
            for lo, idx in by_hi[r]:
                if lo > b1:
                    b2 = b1
                    b1, id1 = lo, idx
                elif lo > b2:
                    b2 = lo
            base += r - b1
            if id1 >= 0:
                bonus[id1] += b1 - b2
        return base + (max(bonus) if m else 0)
