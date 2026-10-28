from typing import *


class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        by_b = [[] for _ in range(n + 1)]
        for i, (x, y) in enumerate(conflictingPairs):
            a, b = min(x, y), max(x, y)
            by_b[b].append((a, i))
        extra = [0] * len(conflictingPairs)
        base = 0
        m1 = m2 = 0
        idx1 = -1
        for r in range(1, n + 1):
            for a, i in by_b[r]:
                if a > m1:
                    m2 = m1
                    m1 = a
                    idx1 = i
                elif a > m2:
                    m2 = a
            if idx1 >= 0:
                extra[idx1] += m1 - m2
            base += r - m1
        return base + max(extra)
