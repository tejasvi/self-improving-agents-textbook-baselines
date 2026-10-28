from typing import *


class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        by_hi = [[] for _ in range(n + 1)]
        for a, b in conflictingPairs:
            lo, hi = (a, b) if a < b else (b, a)
            by_hi[hi].append(lo)
        m1 = 0  # largest left endpoint among pairs with hi <= r (0 = sentinel)
        m2 = 0  # second largest (with multiplicity)
        base = 0
        gain = [0] * (n + 1)
        for r in range(1, n + 1):
            for lo in by_hi[r]:
                if lo > m1:
                    m2 = m1
                    m1 = lo
                elif lo > m2:
                    m2 = lo
            base += r - m1
            gain[m1] += m1 - m2
        return base + max(gain)
