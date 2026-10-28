from typing import List

class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        # prefix sums
        prefix_nums = [0] * n
        prefix_cost = [0] * n
        s = 0
        for i, v in enumerate(nums):
            s += v
            prefix_nums[i] = s
        s = 0
        for i, v in enumerate(cost):
            s += v
            prefix_cost[i] = s
        INF = 10 ** 30
        # dp[t][i] = min cost covering up to index t (inclusive) with i subarrays
        dp = [[INF] * (n + 1) for _ in range(n)]
        # base case: one subarray covering from 0 to t
        for t in range(n):
            dp[t][1] = (prefix_nums[t] + k) * prefix_cost[t]
        # helper functions for convex hull (lower hull, querying minimum)
        from collections import deque
        def eval_line(line, x):
            m, b = line
            return m * x + b
        # determine if l2 is unnecessary between l1 and l3 (all slopes decreasing)
        def is_bad(l1, l2, l3):
            m1, b1 = l1
            m2, b2 = l2
            m3, b3 = l3
            # (b2 - b1) / (m1 - m2) >= (b3 - b1) / (m1 - m3)
            # cross-multiply to avoid division (denominators are positive because m1 > m2 > m3)
            return (b2 - b1) * (m1 - m3) >= (b3 - b1) * (m1 - m2)
        # DP for i >= 2 subarrays
        for i in range(2, n + 1):
            # we need at least i elements to form i subarrays (each at least one element)
            # first possible previous split index
            prev = i - 2
            # initialize hull with line from this previous index
            hull = deque()
            if dp[prev][i - 1] < INF:
                hull.append((-prefix_cost[prev], dp[prev][i - 1]))
            # iterate over possible ending positions t for the i-th subarray
            for t in range(i - 1, n):
                X = prefix_nums[t] + k * i
                # query best line for current X
                while len(hull) >= 2 and eval_line(hull[0], X) >= eval_line(hull[1], X):
                    hull.popleft()
                if hull:
                    best = eval_line(hull[0], X)
                    dp[t][i] = (prefix_nums[t] + k * i) * prefix_cost[t] + best
                # add line for current t to be used as a previous split for future t
                if dp[t][i - 1] < INF:
                    new_line = (-prefix_cost[t], dp[t][i - 1])
                    while len(hull) >= 2 and is_bad(hull[-2], hull[-1], new_line):
                        hull.pop()
                    hull.append(new_line)
        # answer is the minimum over any possible number of subarrays covering the whole array
        ans = INF
        for i in range(1, n + 1):
            ans = min(ans, dp[n - 1][i])
        return ans
