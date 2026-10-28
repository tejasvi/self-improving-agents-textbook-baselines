from collections import deque
from typing import List


class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        # P[r] = nums[0] + ... + nums[r-1], C[r] = cost[0] + ... + cost[r-1]
        P = [0] * (n + 1)
        C = [0] * (n + 1)
        for i in range(n):
            P[i + 1] = P[i] + nums[i]
            C[i + 1] = C[i] + cost[i]

        INF = float("inf")
        # dp_prev[r]: min cost to cover first r elements with t-1 subarrays
        dp_prev = [INF] * (n + 1)
        dp_prev[0] = 0
        best = INF

        for t in range(1, n + 1):
            dp_cur = [INF] * (n + 1)
            # Lines for l: slope -C[l], intercept dp_prev[l].
            # Slopes strictly decrease as l increases; queries x = P[r] + k*t increase with r.
            hull = deque()  # elements: (m, b)

            def value(line, x):
                return line[0] * x + line[1]

            for r in range(1, n + 1):
                l = r - 1
                if dp_prev[l] != INF:
                    m3, b3 = -C[l], dp_prev[l]
                    while len(hull) >= 2:
                        m1, b1 = hull[-2]
                        m2, b2 = hull[-1]
                        # remove line2 if it is never strictly needed
                        if (b3 - b1) * (m1 - m2) <= (b2 - b1) * (m1 - m3):
                            hull.pop()
                        else:
                            break
                    hull.append((m3, b3))
                if not hull:
                    continue
                x = P[r] + k * t
                while len(hull) >= 2 and value(hull[1], x) <= value(hull[0], x):
                    hull.popleft()
                dp_cur[r] = value(hull[0], x) + x * C[r]

            dp_prev = dp_cur
            best = min(best, dp_cur[n])

        return int(best)
