from collections import deque
from typing import List


class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        # P[r] = sum of nums[0..r-1], C[r] = sum of cost[0..r-1]
        P = [0] * (n + 1)
        C = [0] * (n + 1)
        for idx in range(n):
            P[idx + 1] = P[idx] + nums[idx]
            C[idx + 1] = C[idx] + cost[idx]

        INF = float("inf")
        # dp_prev[r]: min cost to cover first r elements with i-1 subarrays
        dp_prev = [INF] * (n + 1)
        dp_prev[0] = 0
        best = INF

        for i in range(1, n + 1):
            dp_cur = [INF] * (n + 1)
            # lines: slope m = -C[j], intercept b = dp_prev[j]
            dq = deque()  # elements (m, b)
            for r in range(1, n + 1):
                j = r - 1
                if dp_prev[j] != INF:
                    m3, b3 = -C[j], dp_prev[j]
                    while len(dq) >= 2:
                        m1, b1 = dq[-2]
                        m2, b2 = dq[-1]
                        # l2 is useless if intersect(l1,l3) <= intersect(l1,l2)
                        if (b3 - b1) * (m1 - m2) <= (b2 - b1) * (m1 - m3):
                            dq.pop()
                        else:
                            break
                    dq.append((m3, b3))
                if not dq:
                    continue
                x = P[r] + k * i
                while len(dq) >= 2 and dq[0][0] * x + dq[0][1] >= dq[1][0] * x + dq[1][1]:
                    dq.popleft()
                m, b = dq[0]
                dp_cur[r] = m * x + b + x * C[r]
            dp_prev = dp_cur
            best = min(best, dp_cur[n])

        return int(best)
