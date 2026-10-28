from typing import *


class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)

        def cost_for_end(k: int, e: int, r: List[int], limit: int) -> int:
            # Edge j (0..n-1) joins vertex j-1 and j (edge 0 = entry from -1).
            # x_j = crossings of edge j: odd if j<=e, even (>=2) if j>e.
            # Vertex j needs x_j + x_{j+1} + [j==e] >= 2*r_j (x_n = 0).
            # Greedy from the left gives the minimum total.
            total = 0
            prev = 0
            for j in range(n):
                if j <= e:
                    v = 1
                    par = 1
                else:
                    v = 2
                    par = 0
                if j >= 1:
                    need = 2 * r[j - 1] - prev - (1 if e == j - 1 else 0)
                    if need > v:
                        v = need
                if (v & 1) != par:
                    v += 1
                total += v
                prev = v
                if total > limit:
                    return total
            # vertex n-1 has no right edge: x_{n-1} + [e==n-1] >= 2*r_{n-1}
            # (already enforced above only through the right-edge term x_n=0)
            need_last = 2 * r[n - 1] - (1 if e == n - 1 else 0)
            if prev < need_last:
                # bump x_{n-1} to satisfy the constraint, keeping parity
                v = need_last
                if (v & 1) != (1 if n - 1 <= e else 0):
                    v += 1
                total += v - prev
            return total

        def feasible(k: int) -> bool:
            r = [(k + p - 1) // p for p in points]
            cands = {n - 1, n - 2, -1, 0}
            am = max(range(n), key=lambda i: r[i])
            cands |= {am - 1, am, am + 1}
            for e in cands:
                if -1 <= e < n:
                    if e == -1:
                        continue
                    if cost_for_end(k, e, r, m) <= m:
                        return True
            return False

        lo, hi = 0, m * max(points) // n + 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo
