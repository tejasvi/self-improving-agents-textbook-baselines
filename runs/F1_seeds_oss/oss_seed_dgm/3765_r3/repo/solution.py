import sys
from typing import List

class Line:
    __slots__ = ("m", "b")
    def __init__(self, m: int, b: int):
        self.m = m  # slope
        self.b = b  # intercept
    def value(self, x: int) -> int:
        return self.m * x + self.b

def is_bad(l1: Line, l2: Line, l3: Line) -> bool:
    # Return True if l2 is unnecessary between l1 and l3.
    # Compare (b3 - b1)/(m1 - m3) <= (b2 - b1)/(m1 - m2)
    # To avoid division, cross-multiply. Slopes are decreasing (more negative).
    return (l3.b - l1.b) * (l1.m - l2.m) <= (l2.b - l1.b) * (l1.m - l3.m)

class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        preNum = [0] * n
        preCost = [0] * n
        s = 0
        for i, v in enumerate(nums):
            s += v
            preNum[i] = s
        s = 0
        for i, v in enumerate(cost):
            s += v
            preCost[i] = s

        INF = 10**18
        # dp_prev[i] = min cost to cover up to i with (j-1) subarrays
        dp_prev = [INF] * n
        # Base for j = 1 (one subarray covering 0..i)
        for i in range(n):
            dp_prev[i] = (preNum[i] + k * 1) * preCost[i]
        answer = dp_prev[-1]
        # Iterate over possible number of subarrays j = 2..n
        for j in range(2, n + 1):
            dp_curr = [INF] * n
            from collections import deque
            hull = deque()
            # Insert line for p = j-2 (the smallest possible previous index)
            p = j - 2
            # line: slope = -preCost[p], intercept = dp_prev[p]
            hull.append(Line(-preCost[p], dp_prev[p]))
            for i in range(j - 1, n):
                # before querying for i, ensure lines for all p < i are added.
                if i - 1 >= j - 2:
                    # we already added line for p = i-1 at previous iteration's end.
                    # That's handled after computing dp for i-1.
                    pass
                # Query hull for minimum value at X = preNum[i] + k * j
                X = preNum[i] + k * j
                while len(hull) >= 2 and hull[0].value(X) >= hull[1].value(X):
                    hull.popleft()
                best = hull[0].value(X)
                dp_curr[i] = (preNum[i] + k * j) * preCost[i] + best
                # After processing i, add line for p = i (to be used for future i+1)
                # Only if i can serve as a cut for next positions (i.e., there are enough remaining elements)
                if i < n - 1:
                    new_line = Line(-preCost[i], dp_prev[i])
                    # Maintain lower hull: remove last while bad
                    while len(hull) >= 2 and is_bad(hull[-2], hull[-1], new_line):
                        hull.pop()
                    hull.append(new_line)
            dp_prev = dp_curr
            answer = min(answer, dp_prev[-1])
        return answer
