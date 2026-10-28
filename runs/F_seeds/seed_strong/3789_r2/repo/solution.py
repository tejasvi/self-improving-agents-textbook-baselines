from typing import *


class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        m = len(conflictingPairs)
        by_max = [[] for _ in range(n + 1)]
        for i, (a, b) in enumerate(conflictingPairs):
            lo, hi = (a, b) if a < b else (b, a)
            by_max[hi].append((lo, i))

        extra = [0] * m
        base = 0
        top1 = 0      # largest min value among pairs with max <= r
        idx1 = -1     # index of pair achieving top1
        top2 = 0      # second largest (from a different pair)
        for r in range(1, n + 1):
            for lo, i in by_max[r]:
                if lo > top1:
                    top2 = top1
                    top1 = lo
                    idx1 = i
                elif lo > top2:
                    top2 = lo
            base += r - top1
            if idx1 >= 0:
                extra[idx1] += top1 - top2
        return base + max(extra)
