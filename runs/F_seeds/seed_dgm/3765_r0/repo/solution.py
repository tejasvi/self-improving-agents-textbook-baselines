from collections import deque
from typing import List


class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        # S[r] = nums[0] + ... + nums[r-1]; C[r] = cost[0] + ... + cost[r-1]
        S = [0] * (n + 1)
        C = [0] * (n + 1)
        for i in range(n):
            S[i + 1] = S[i] + nums[i]
            C[i + 1] = C[i] + cost[i]

        INF = None
        # prev[r]: min cost splitting first r elements into j-1 subarrays
        prev = [INF] * (n + 1)
        prev[0] = 0
        best = INF

        for j in range(1, n + 1):
            cur = [INF] * (n + 1)
            # lines: slope = -C[l-1], intercept = prev[l-1] - k*j*C[l-1]
            dq = deque()  # elements: (slope, intercept)
            kj = k * j

            def bad(l1, l2, l3):
                # True if l2 is unnecessary given l1, l3 (slopes decreasing: m1 > m2 > m3)
                # intersection(l1,l3) <= intersection(l1,l2)
                m1, b1 = l1
                m2, b2 = l2
                m3, b3 = l3
                return (b3 - b1) * (m1 - m2) <= (b2 - b1) * (m1 - m3)

            for r in range(1, n + 1):
                l = r  # line for l, uses prev[l-1]
                if prev[l - 1] is not None:
                    line = (-C[l - 1], prev[l - 1] - kj * C[l - 1])
                    while len(dq) >= 2 and bad(dq[-2], dq[-1], line):
                        dq.pop()
                    dq.append(line)
                if not dq:
                    continue
                x = S[r]
                while len(dq) >= 2 and dq[0][0] * x + dq[0][1] >= dq[1][0] * x + dq[1][1]:
                    dq.popleft()
                m, b = dq[0]
                cur[r] = (x + kj) * C[r] + m * x + b
            prev = cur
            if cur[n] is not None and (best is None or cur[n] < best):
                best = cur[n]
        return best
