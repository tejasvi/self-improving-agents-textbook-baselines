from typing import *
from collections import deque


class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        # S[r]: prefix sum of nums (first r), C[r]: prefix sum of cost (first r)
        S = [0] * (n + 1)
        C = [0] * (n + 1)
        for i in range(n):
            S[i + 1] = S[i] + nums[i]
            C[i + 1] = C[i] + cost[i]

        INF = float("inf")
        # prev[l]: min cost to partition first l elements into (layer-1) segments
        prev = [INF] * (n + 1)
        prev[0] = 0
        best = INF

        for i in range(1, n + 1):
            cur = [INF] * (n + 1)
            # lines: slope -C[l], intercept prev[l], query x = S[r] + k*i
            # value = intercept + x * (-C[l]) ; deque holds (slope, intercept)
            dq = deque()
            for r in range(1, n + 1):
                l = r - 1
                if prev[l] < INF:
                    m = -C[l]
                    b = prev[l]
                    # slopes strictly decreasing; maintain lower envelope for min
                    while len(dq) >= 2:
                        m1, b1 = dq[-2]
                        m2, b2 = dq[-1]
                        # line2 useless if intersection(1,3) <= intersection(1,2)
                        # (b - b1)*(m1 - m2) <= (b2 - b1)*(m1 - m)
                        if (b - b1) * (m1 - m2) <= (b2 - b1) * (m1 - m):
                            dq.pop()
                        else:
                            break
                    dq.append((m, b))
                if not dq:
                    continue
                x = S[r] + k * i
                while len(dq) >= 2:
                    m1, b1 = dq[0]
                    m2, b2 = dq[1]
                    if m2 * x + b2 <= m1 * x + b1:
                        dq.popleft()
                    else:
                        break
                m1, b1 = dq[0]
                cur[r] = m1 * x + b1 + x * C[r]
            prev = cur
            if prev[n] < best:
                best = prev[n]
        return int(best)
