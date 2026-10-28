from typing import *


class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        m = len(conflictingPairs)
        extra = [0] * m
        idx_groups = [[] for _ in range(n + 1)]
        for i, (a, b) in enumerate(conflictingPairs):
            hi = max(a, b)
            idx_groups[hi].append(i)
        b1 = 0
        b2 = 0
        id1 = -1
        base = 0
        for r in range(1, n + 1):
            for i in idx_groups[r]:
                a, b = conflictingPairs[i]
                v = min(a, b)
                if v > b1:
                    b2 = b1
                    b1 = v
                    id1 = i
                elif v > b2:
                    b2 = v
            base += r - b1
            if id1 >= 0:
                extra[id1] += b1 - b2
        return base + (max(extra) if m else 0)
