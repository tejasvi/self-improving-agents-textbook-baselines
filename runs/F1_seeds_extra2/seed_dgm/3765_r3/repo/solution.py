from typing import List


class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        P = [0] * (n + 1)  # prefix sums of nums
        C = [0] * (n + 1)  # prefix sums of cost
        for i in range(n):
            P[i + 1] = P[i] + nums[i]
            C[i + 1] = C[i] + cost[i]

        INF = float("inf")
        prev = [INF] * (n + 1)
        prev[0] = 0
        best = INF

        for j in range(1, n + 1):
            cur = [INF] * (n + 1)
            # Monotone hull of lines y = m*x + b with m = -C[l], b = prev[l].
            # Slopes strictly decrease as l increases; queries x = P[i] + k*j increase.
            ms, bs = [], []
            head = 0
            for i in range(1, n + 1):
                # add line for l = i-1 if reachable
                l = i - 1
                if prev[l] != INF:
                    m3, b3 = -C[l], prev[l]
                    while len(ms) - head >= 2:
                        m1, b1 = ms[-2], bs[-2]
                        m2, b2 = ms[-1], bs[-1]
                        # remove l2 if it is never strictly optimal
                        if (b3 - b1) * (m1 - m2) <= (b2 - b1) * (m1 - m3):
                            ms.pop()
                            bs.pop()
                        else:
                            break
                    ms.append(m3)
                    bs.append(b3)
                if len(ms) - head == 0:
                    continue
                x = P[i] + k * j
                while len(ms) - head >= 2 and ms[head + 1] * x + bs[head + 1] <= ms[head] * x + bs[head]:
                    head += 1
                val = ms[head] * x + bs[head] + x * C[i]
                cur[i] = val
            prev = cur
            if prev[n] < best:
                best = prev[n]
        return int(best)
