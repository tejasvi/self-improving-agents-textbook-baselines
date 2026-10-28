from typing import List


class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        m = len(conflictingPairs)
        # Group pairs by their larger endpoint (right end), store smaller endpoint.
        by_right = [[] for _ in range(n + 1)]
        for i, (x, y) in enumerate(conflictingPairs):
            a, b = min(x, y), max(x, y)
            by_right[b].append((a, i))

        base = 0
        extra = [0] * m
        top1 = 0      # largest a among pairs with b <= r
        top1_idx = -1
        top2 = 0      # second largest a (multiset sense)

        for r in range(1, n + 1):
            for a, i in by_right[r]:
                if a >= top1:
                    top2 = top1
                    top1 = a
                    top1_idx = i
                elif a > top2:
                    top2 = a
            base += r - top1
            if top1_idx != -1:
                extra[top1_idx] += top1 - top2

        return base + max(extra)
