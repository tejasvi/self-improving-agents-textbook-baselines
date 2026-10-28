from bisect import bisect_left, bisect_right
from typing import List


class Solution:
    def minimumMoves(self, nums: List[int], k: int, maxChanges: int) -> int:
        n = len(nums)
        p = [i for i in range(n) if nums[i] == 1]
        total = len(p)
        # prefix sums of positions
        P = [0] * (total + 1)
        for j, x in enumerate(p):
            P[j + 1] = P[j] + x

        L = max(0, k - maxChanges)   # minimum number of existing ones to pick
        M = min(k, total)            # maximum number of existing ones usable

        def nearest_sum(i, m, c):
            # sum of distances of the m nearest ones to i; c = #ones at positions < i
            nl = c
            nr = total - c
            lo = max(0, m - nr)
            hi = min(m, nl)

            def SA(a):  # a nearest on the left
                return a * i - (P[c] - P[c - a])

            def SB(b):  # b nearest on the right
                return (P[c + b] - P[c]) - b * i

            # find smallest a in [lo, hi) with A[a] >= B[m-a-1]; else hi
            l, r = lo, hi
            while l < r:
                mid = (l + r) // 2
                A = i - p[c - 1 - mid]
                B = p[c + (m - mid - 1)] - i
                if A >= B:
                    r = mid
                else:
                    l = mid + 1
            a = l
            return SA(a) + SB(m - a)

        best = None
        for i in range(n):
            c = bisect_left(p, i)
            cnt = bisect_right(p, i + 1) - bisect_left(p, i - 1)
            m = min(max(cnt, L), M)
            cost = nearest_sum(i, m, c) + 2 * (k - m)
            if best is None or cost < best:
                best = cost
        return best
