from collections import deque
from typing import List


class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        # P[j] = nums[0] + ... + nums[j-1]; C[j] = cost[0] + ... + cost[j-1]
        P = [0] * (n + 1)
        C = [0] * (n + 1)
        for j in range(n):
            P[j + 1] = P[j] + nums[j]
            C[j + 1] = C[j] + cost[j]

        # dp_i[j] = min over l of dp_{i-1}[l] + (P[j] + k*i) * (C[j] - C[l])
        # Lines: slope -C[l] (strictly decreasing), intercept dp_{i-1}[l];
        # queries x = P[j] + k*i increase with j -> monotone convex hull trick.
        prev = [None] * (n + 1)
        prev[0] = 0
        answer = None

        for i in range(1, n + 1):
            cur = [None] * (n + 1)
            hull = deque()  # lines (slope, intercept)
            for j in range(1, n + 1):
                l = j - 1
                if prev[l] is not None:
                    m, b = -C[l], prev[l]
                    while len(hull) >= 2:
                        ma, ba = hull[-2]
                        mb, bb = hull[-1]
                        if (b - ba) * (ma - mb) <= (bb - ba) * (ma - m):
                            hull.pop()
                        else:
                            break
                    hull.append((m, b))
                if not hull:
                    continue
                x = P[j] + k * i
                while len(hull) >= 2 and hull[1][0] * x + hull[1][1] <= hull[0][0] * x + hull[0][1]:
                    hull.popleft()
                cur[j] = hull[0][0] * x + hull[0][1] + C[j] * x
            prev = cur
            if prev[n] is not None and (answer is None or prev[n] < answer):
                answer = prev[n]
        return answer
