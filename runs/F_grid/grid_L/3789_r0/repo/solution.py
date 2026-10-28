from typing import List


class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        m = len(conflictingPairs)
        by_right = [[] for _ in range(n + 1)]
        for idx, (x, y) in enumerate(conflictingPairs):
            a, b = min(x, y), max(x, y)
            by_right[b].append((a, idx))

        # top two (value, index) entries over pairs with right endpoint <= r
        top = []  # sorted desc by value, at most 2 entries
        base = 0
        gain = [0] * m
        for r in range(1, n + 1):
            for cand in by_right[r]:
                top.append(cand)
            top.sort(key=lambda t: -t[0])
            del top[2:]
            m1, id1 = (top[0] if len(top) > 0 else (0, -1))
            m2 = top[1][0] if len(top) > 1 else 0
            base += r - m1
            if id1 >= 0:
                gain[id1] += m1 - m2

        return base + max(gain)
