from typing import List
from collections import deque


class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        # Prefix sums: S[i] = sum(nums[0..i-1]), C[i] = sum(cost[0..i-1])
        S = [0] * (n + 1)
        C = [0] * (n + 1)
        for i in range(n):
            S[i + 1] = S[i] + nums[i]
            C[i + 1] = C[i] + cost[i]

        INF = float("inf")
        # prev[l] = min cost to split first l elements into (j-1) segments
        prev = [INF] * (n + 1)
        prev[0] = 0
        best = INF

        for j in range(1, n + 1):
            cur = [INF] * (n + 1)
            # Lines: slope m = -C[l], intercept b = prev[l] - k*j*C[l], query x = S[i].
            # Slopes strictly decrease as l grows (cost >= 1); queries x = S[i] strictly increase.
            hull = deque()  # elements (m, b)
            for i in range(j, n + 1):
                l = i - 1
                if prev[l] < INF:
                    m = -C[l]
                    b = prev[l] - k * j * C[l]
                    # Remove back lines that become unnecessary
                    while len(hull) >= 2:
                        m1, b1 = hull[-2]
                        m2, b2 = hull[-1]
                        # l2 useless if (b3-b1)*(m1-m2) <= (b2-b1)*(m1-m3)
                        if (b - b1) * (m1 - m2) <= (b2 - b1) * (m1 - m):
                            hull.pop()
                        else:
                            break
                    hull.append((m, b))
                if not hull:
                    continue
                x = S[i]
                # Pop front lines that are no better at x (x increasing)
                while len(hull) >= 2 and hull[0][0] * x + hull[0][1] >= hull[1][0] * x + hull[1][1]:
                    hull.popleft()
                val = hull[0][0] * x + hull[0][1]
                cur[i] = val + (S[i] + k * j) * C[i]
            prev = cur
            if prev[n] < best:
                best = prev[n]
        return int(best)
