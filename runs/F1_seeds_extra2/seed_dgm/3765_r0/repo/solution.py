from collections import deque
from typing import List


class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        # S[r] = nums[0..r-1] sum, C[r] = cost[0..r-1] sum
        S = [0] * (n + 1)
        C = [0] * (n + 1)
        for i in range(n):
            S[i + 1] = S[i] + nums[i]
            C[i + 1] = C[i] + cost[i]

        INF = None
        prev = [INF] * (n + 1)
        prev[0] = 0  # zero subarrays covering zero elements
        best = None

        for j in range(1, n + 1):
            cur = [INF] * (n + 1)
            # Lines: slope -C[l], intercept prev[l]; added in order of l
            # (slopes strictly decreasing). Query x = S[r] + k*j, increasing in r.
            dq = deque()  # elements (slope, intercept)

            def bad(l1, l2, l3):
                # l2 is unnecessary if intersection(l1,l3) <= intersection(l1,l2)
                # slopes m1 > m2 > m3, intercepts b
                m1, b1 = l1
                m2, b2 = l2
                m3, b3 = l3
                return (b3 - b1) * (m1 - m2) <= (b2 - b1) * (m1 - m3)

            for r in range(j, n + 1):
                l = r - 1
                if prev[l] is not None:
                    line = (-C[l], prev[l])
                    while len(dq) >= 2 and bad(dq[-2], dq[-1], line):
                        dq.pop()
                    dq.append(line)
                if not dq:
                    continue
                x = S[r] + k * j
                while len(dq) >= 2 and dq[0][0] * x + dq[0][1] >= dq[1][0] * x + dq[1][1]:
                    dq.popleft()
                m, b = dq[0]
                cur[r] = m * x + b + x * C[r]
            prev = cur
            if cur[n] is not None and (best is None or cur[n] < best):
                best = cur[n]
        return best
