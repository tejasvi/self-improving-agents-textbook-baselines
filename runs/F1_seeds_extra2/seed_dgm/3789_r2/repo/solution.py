from typing import List


class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        # For each right endpoint r, valid subarrays ending at r = r - L(r),
        # where L(r) = max over pairs (lo, hi) with hi <= r of lo.
        by_hi = [[] for _ in range(n + 1)]
        for idx, (a, b) in enumerate(conflictingPairs):
            lo, hi = (a, b) if a < b else (b, a)
            by_hi[hi].append((lo, idx))

        m = len(conflictingPairs)
        gain = [0] * m
        top1v, top1id, top2v = 0, -1, 0
        base = 0
        for r in range(1, n + 1):
            for v, idx in by_hi[r]:
                if v > top1v:
                    top2v = top1v
                    top1v, top1id = v, idx
                elif v > top2v:
                    top2v = v
            base += r - top1v
            if top1id >= 0:
                gain[top1id] += top1v - top2v

        return base + max(gain)
