from typing import List


class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        # Group pairs by hi = max(a, b); store lo = min(a, b).
        by_hi = [[] for _ in range(n + 1)]
        for a, b in conflictingPairs:
            lo, hi = (a, b) if a < b else (b, a)
            by_hi[hi].append(lo)

        base = 0
        gain = [0] * (n + 1)  # gain[lo value] when removing the pair(s) with that lo
        L1 = 0  # largest lo among pairs with hi <= r
        L2 = 0  # second largest (multiset)
        for r in range(1, n + 1):
            for lo in by_hi[r]:
                if lo >= L1:
                    L2 = L1
                    L1 = lo
                elif lo > L2:
                    L2 = lo
            base += r - L1
            if L1 > 0:
                gain[L1] += L1 - L2
        return base + max(gain)
