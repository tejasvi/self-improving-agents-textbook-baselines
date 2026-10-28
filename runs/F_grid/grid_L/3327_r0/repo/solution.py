from bisect import bisect_left
from typing import List


class Solution:
    def minimumMoves(self, nums: List[int], k: int, maxChanges: int) -> int:
        n = len(nums)
        p = [i for i, v in enumerate(nums) if v == 1]
        m = len(p)
        P = [0] * (m + 1)
        for i, v in enumerate(p):
            P[i + 1] = P[i] + v

        cap = min(k, m)
        L = max(0, k - maxChanges)
        best = None

        for a in range(n):
            i = bisect_left(p, a)  # p[:i] < a <= p[i:]
            nl = i
            nr = m - i
            # number of ones within distance 2 of a
            lo = bisect_left(p, a - 2)
            hi = bisect_left(p, a + 3)
            c2 = hi - lo
            x = min(max(c2, L), cap)

            # sum of distances of the x nearest ones to a
            jlo = max(0, x - nr)
            jhi = min(x, nl)

            def f_delta(j):
                # cost change from taking j+1 left and x-j-1 right, vs j left, x-j right
                return (a - p[i - j - 1]) - (p[i + x - j - 1] - a)

            # find smallest j in [jlo, jhi) with delta >= 0; else jhi
            l, r = jlo, jhi
            while l < r:
                mid = (l + r) // 2
                if f_delta(mid) >= 0:
                    r = mid
                else:
                    l = mid + 1
            j = l
            left_sum = a * j - (P[i] - P[i - j])
            rc = x - j
            right_sum = (P[i + rc] - P[i]) - a * rc
            cost = left_sum + right_sum + 2 * (k - x)
            if best is None or cost < best:
                best = cost
        return best
