from typing import List
import math

class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        # prefix sums
        prefix_num = [0] * n
        prefix_cost = [0] * n
        s = 0
        c = 0
        for i in range(n):
            s += nums[i]
            c += cost[i]
            prefix_num[i] = s
            prefix_cost[i] = c

        INF = 10**30
        # dp_prev[j] = min cost to partition first j+1 elements using (i-1) segments
        dp_prev = [INF] * n
        # i = 1 case
        for j in range(n):
            x = prefix_num[j] + k * 1
            dp_prev[j] = x * prefix_cost[j]
        answer = dp_prev[-1]

        # Helper line class for convex hull (min)
        class Line:
            __slots__ = ('m', 'b')
            def __init__(self, m: int, b: int):
                self.m = m  # slope
                self.b = b  # intercept
            def value(self, x: int) -> int:
                return self.m * x + self.b
        # Intersection point (as float) where l1 and l2 give same value
        def intersect_x(l1: Line, l2: Line) -> float:
            # l1.m != l2.m guaranteed as slopes are strictly decreasing (cost positive)
            return (l2.b - l1.b) / (l1.m - l2.m)

        # Iterate over possible number of segments i (starting from 2)
        for seg in range(2, n + 1):
            dp_cur = [INF] * n
            # deque for convex hull lines
            from collections import deque
            hull = deque()
            # we can only start at position seg-1 (minimum index to have seg segments)
            # first line corresponds to p = seg-2
            p_start = seg - 2
            if p_start >= 0 and dp_prev[p_start] < INF:
                hull.append(Line(-prefix_cost[p_start], dp_prev[p_start]))
            # iterate j from seg-1 to n-1
            for j in range(seg - 1, n):
                # add line for p = j-1 before querying for current j (except when j == seg-1, line already added)
                if j - 1 > p_start:
                    p = j - 1
                    if dp_prev[p] < INF:
                        new_line = Line(-prefix_cost[p], dp_prev[p])
                        # maintain decreasing slopes (more negative) -> slopes are -prefix_cost[p]
                        # Since prefix_cost is non‑decreasing, -prefix_cost is non‑increasing, satisfying order.
                        while len(hull) >= 2 and intersect_x(hull[-2], hull[-1]) >= intersect_x(hull[-1], new_line):
                            hull.pop()
                        hull.append(new_line)
                # query hull for best line at x = prefix_num[j] + k*seg
                if not hull:
                    continue
                x = prefix_num[j] + k * seg
                # pop front while next line gives better (smaller) value
                while len(hull) >= 2 and hull[0].value(x) >= hull[1].value(x):
                    hull.popleft()
                best = hull[0].value(x)  # this is min_{p<j} dp_prev[p] - x * prefix_cost[p]
                dp_cur[j] = x * prefix_cost[j] + best
            dp_prev = dp_cur
            answer = min(answer, dp_prev[-1])
        return answer
