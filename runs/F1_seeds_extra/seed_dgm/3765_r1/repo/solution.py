from typing import List
from collections import deque


class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        # P[r] = nums[0] + ... + nums[r-1]; C[r] = cost[0] + ... + cost[r-1]
        P = [0] * (n + 1)
        C = [0] * (n + 1)
        for i in range(n):
            P[i + 1] = P[i] + nums[i]
            C[i + 1] = C[i] + cost[i]

        INF = None
        prev = [INF] * (n + 1)  # f[j-1][*]
        prev[0] = 0
        best_answer = INF

        for j in range(1, n + 1):
            cur = [INF] * (n + 1)
            # Convex hull of lines (m, b), slopes strictly decreasing, min query
            hull = deque()

            def bad(l1, l2, l3):
                # l2 is useless if intersection(l1,l3) <= intersection(l1,l2)
                m1, b1 = l1
                m2, b2 = l2
                m3, b3 = l3
                return (b3 - b1) * (m1 - m2) <= (b2 - b1) * (m1 - m3)

            for r in range(1, n + 1):
                # add line for l = r, i.e. previous prefix index r-1
                if prev[r - 1] is not INF:
                    line = (-C[r - 1], prev[r - 1])
                    while len(hull) >= 2 and bad(hull[-2], hull[-1], line):
                        hull.pop()
                    hull.append(line)
                if not hull:
                    continue
                x = P[r] + k * j
                while len(hull) >= 2:
                    m1, b1 = hull[0]
                    m2, b2 = hull[1]
                    if m1 * x + b1 >= m2 * x + b2:
                        hull.popleft()
                    else:
                        break
                m, b = hull[0]
                cur[r] = m * x + b + x * C[r]
            if cur[n] is not INF:
                if best_answer is INF or cur[n] < best_answer:
                    best_answer = cur[n]
            prev = cur

        return best_answer
