"""Solution for minimum-cost-to-divide-array-into-subarrays.

We use DP with convex hull optimization.
"""
from typing import List
import math

class Line:
    __slots__ = ("m", "b")
    def __init__(self, m: int, b: int):
        self.m = m
        self.b = b
    def value(self, x: int) -> int:
        return self.m * x + self.b

def is_bad(l1: Line, l2: Line, l3: Line) -> bool:
    # Return True if l2 is unnecessary between l1 and l3.
    # (b2 - b1)/(m1 - m2) >= (b3 - b2)/(m2 - m3)
    return (l2.b - l1.b) * (l2.m - l3.m) >= (l3.b - l2.b) * (l1.m - l2.m)

class ConvexHull:
    """Maintains lower hull for lines added with decreasing slopes.
    Queries are made with non‑decreasing x.
    """
    def __init__(self):
        self.hull: List[Line] = []
        self.ptr = 0  # pointer for queries with increasing x
    def add_line(self, m: int, b: int):
        new_line = Line(m, b)
        # slopes must be strictly decreasing (m smaller each time)
        while len(self.hull) >= 2 and is_bad(self.hull[-2], self.hull[-1], new_line):
            self.hull.pop()
        self.hull.append(new_line)
    def query(self, x: int) -> int:
        # Move pointer to the best line for current x
        if not self.hull:
            return math.inf
        while self.ptr + 1 < len(self.hull) and self.hull[self.ptr].value(x) >= self.hull[self.ptr + 1].value(x):
            self.ptr += 1
        return self.hull[self.ptr].value(x)
    def reset(self):
        self.hull.clear()
        self.ptr = 0

class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        # prefix sums
        S = [0] * (n + 1)  # sum of nums
        C = [0] * (n + 1)  # sum of cost
        for i in range(n):
            S[i + 1] = S[i] + nums[i]
            C[i + 1] = C[i] + cost[i]

        INF = 10 ** 30
        # dp_prev[j] = min cost for first j elements using cnt-1 subarrays
        dp_prev = [INF] * (n + 1)
        dp_prev[0] = 0
        answer = INF
        # maximum possible subarrays is n
        for cnt in range(1, n + 1):
            dp_cur = [INF] * (n + 1)
            hull = ConvexHull()
            # initial line from l = 0
            hull.add_line(-C[0], dp_prev[0])  # slope = -C[l], intercept = dp_prev[l]
            for r in range(1, n + 1):
                # query best previous cut
                x = S[r] + k * cnt
                best = hull.query(x)
                if best != INF:
                    dp_cur[r] = (S[r] + k * cnt) * C[r] + best
                # add line for this position to be used for future r
                # line corresponds to l = r
                if dp_prev[r] < INF:
                    hull.add_line(-C[r], dp_prev[r])
            answer = min(answer, dp_cur[n])
            dp_prev = dp_cur
        return answer
