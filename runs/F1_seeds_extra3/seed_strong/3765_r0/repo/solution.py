from typing import *
from collections import deque


class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        P = [0] * (n + 1)
        C = [0] * (n + 1)
        for i in range(n):
            P[i + 1] = P[i] + nums[i]
            C[i + 1] = C[i] + cost[i]
        INF = float("inf")
        # dp_prev[r]: min cost to split first r elements into (j-1) segments
        dp_prev = [INF] * (n + 1)
        dp_prev[0] = 0
        best = INF
        for j in range(1, n + 1):
            cur = [INF] * (n + 1)
            # lines: slope -C[l], intercept dp_prev[l]; query x = P[r] + k*j
            sl = deque()
            ic = deque()
            for r in range(1, n + 1):
                l = r - 1
                if dp_prev[l] != INF:
                    s3 = -C[l]
                    b3 = dp_prev[l]
                    while len(sl) >= 2:
                        s1, b1 = sl[-2], ic[-2]
                        s2, b2 = sl[-1], ic[-1]
                        # line 2 useless if x13 <= x12
                        if (b3 - b1) * (s1 - s2) <= (b2 - b1) * (s1 - s3):
                            sl.pop()
                            ic.pop()
                        else:
                            break
                    sl.append(s3)
                    ic.append(b3)
                if not sl:
                    continue
                x = P[r] + k * j
                while len(sl) >= 2 and sl[1] * x + ic[1] <= sl[0] * x + ic[0]:
                    sl.popleft()
                    ic.popleft()
                cur[r] = sl[0] * x + ic[0] + x * C[r]
            if cur[n] < best:
                best = cur[n]
            dp_prev = cur
        return int(best)
