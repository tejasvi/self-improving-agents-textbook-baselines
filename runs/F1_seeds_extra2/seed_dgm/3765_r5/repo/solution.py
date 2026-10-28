from typing import List
from collections import deque


class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        # P[r]: prefix sum of nums up to index r-1 (length r); C likewise for cost.
        P = [0] * (n + 1)
        C = [0] * (n + 1)
        for i in range(n):
            P[i + 1] = P[i] + nums[i]
            C[i + 1] = C[i] + cost[i]

        INF = float("inf")
        prev = [INF] * (n + 1)
        prev[0] = 0
        best = INF

        for i in range(1, n + 1):
            cur = [INF] * (n + 1)
            # Lines: slope m = -C[l], intercept b = prev[l], for valid l.
            # Slopes strictly decrease as l increases (cost >= 1).
            hull_m = []
            hull_b = []
            head = 0
            for r in range(1, n + 1):
                l = r - 1
                if prev[l] != INF:
                    m3, b3 = -C[l], prev[l]
                    while len(hull_m) - head >= 2:
                        m1, b1 = hull_m[-2], hull_b[-2]
                        m2, b2 = hull_m[-1], hull_b[-1]
                        # l2 is unnecessary if intersect(l1,l3) <= intersect(l1,l2)
                        if (b3 - b1) * (m1 - m2) <= (b2 - b1) * (m1 - m3):
                            hull_m.pop()
                            hull_b.pop()
                        else:
                            break
                    hull_m.append(m3)
                    hull_b.append(b3)
                if len(hull_m) > head:
                    x = P[r] + k * i
                    while (len(hull_m) - head >= 2 and
                           hull_m[head + 1] * x + hull_b[head + 1]
                           <= hull_m[head] * x + hull_b[head]):
                        head += 1
                    val = hull_m[head] * x + hull_b[head] + x * C[r]
                    cur[r] = val
            best = min(best, cur[n])
            prev = cur
        return int(best)
