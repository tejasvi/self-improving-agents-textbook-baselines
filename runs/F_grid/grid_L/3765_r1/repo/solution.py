from typing import List
from collections import deque


class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        # P[r]: sum of nums[0..r-1], C[r]: sum of cost[0..r-1]
        P = [0] * (n + 1)
        C = [0] * (n + 1)
        for idx in range(n):
            P[idx + 1] = P[idx] + nums[idx]
            C[idx + 1] = C[idx] + cost[idx]

        INF = float("inf")
        prev = [INF] * (n + 1)
        prev[0] = 0
        best = INF

        for i in range(1, n + 1):
            cur = [INF] * (n + 1)
            # Lines: slope -C[l], intercept prev[l], for l with finite prev[l].
            hull = deque()  # elements: (slope, intercept, l)
            for r in range(1, n + 1):
                l = r - 1
                if prev[l] != INF:
                    m3 = -C[l]
                    b3 = prev[l]
                    # maintain decreasing slopes; remove useless middle lines
                    while len(hull) >= 2:
                        m1, b1, _ = hull[-2]
                        m2, b2, _ = hull[-1]
                        if (b3 - b1) * (m1 - m2) <= (b2 - b1) * (m1 - m3):
                            hull.pop()
                        else:
                            break
                    hull.append((m3, b3, l))
                if not hull:
                    continue
                x = P[r] + k * i
                while len(hull) >= 2:
                    m1, b1, _ = hull[0]
                    m2, b2, _ = hull[1]
                    if m2 * x + b2 <= m1 * x + b1:
                        hull.popleft()
                    else:
                        break
                m, b, _ = hull[0]
                cur[r] = m * x + b + x * C[r]
            if cur[n] < best:
                best = cur[n]
            prev = cur
        return int(best)
