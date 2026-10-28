from typing import *
from collections import deque


class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        S = [0] * (n + 1)
        C = [0] * (n + 1)
        for i in range(n):
            S[i + 1] = S[i] + nums[i]
            C[i + 1] = C[i] + cost[i]

        INF = None
        # prev[l]: min cost to split first l elements into (layer-1) segments
        prev = [INF] * (n + 1)
        prev[0] = 0
        best = INF

        for i in range(1, n + 1):
            cur = [INF] * (n + 1)
            # lines: slope m = -C[l], intercept b = prev[l]; query x = S[r] + k*i
            # min over lines of m*x + b, slopes strictly decreasing as l increases
            dq = deque()  # elements: (m, b)
            for r in range(1, n + 1):
                l = r - 1
                if prev[l] is not None:
                    m = -C[l]
                    b = prev[l]
                    # remove back lines that are unnecessary
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
                while len(dq) >= 2 and dq[0][0] * x + dq[0][1] >= dq[1][0] * x + dq[1][1]:
                    dq.popleft()
                m, b = dq[0]
                val = m * x + b + x * C[r]
                cur[r] = val
            prev = cur
            if cur[n] is not None and (best is None or cur[n] < best):
                best = cur[n]
        return best
