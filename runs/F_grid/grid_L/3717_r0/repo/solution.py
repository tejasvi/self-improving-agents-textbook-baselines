from typing import List


class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        vals = sorted(set(nums))
        m = len(vals)
        rank = {v: i + 1 for i, v in enumerate(vals)}  # 1-based

        cnt_tree = [0] * (m + 1)
        sum_tree = [0] * (m + 1)
        LOG = 1
        while (1 << LOG) <= m:
            LOG += 1

        def update(i, dc, dv):
            while i <= m:
                cnt_tree[i] += dc
                sum_tree[i] += dv
                i += i & -i

        def kth(target):
            # smallest index p (1-based) with prefix count >= target
            pos = 0
            rem = target
            for b in range(LOG, -1, -1):
                np_ = pos + (1 << b)
                if np_ <= m and cnt_tree[np_] < rem:
                    pos = np_
                    rem -= cnt_tree[np_]
            return pos + 1

        def prefix(i):
            c = s = 0
            while i > 0:
                c += cnt_tree[i]
                s += sum_tree[i]
                i -= i & -i
            return c, s

        # cost[l] = min cost to make nums[l..l+x-1] equal
        INF = float("inf")
        cost = [0] * (n - x + 1)
        total_sum = 0
        target = (x + 1) // 2
        for i in range(n):
            r = rank[nums[i]]
            update(r, 1, nums[i])
            total_sum += nums[i]
            if i >= x:
                out = nums[i - x]
                update(rank[out], -1, -out)
                total_sum -= out
            if i >= x - 1:
                p = kth(target)
                med = vals[p - 1]
                cl, sl = prefix(p)
                cr = x - cl
                sr = total_sum - sl
                cost[i - x + 1] = med * cl - sl + sr - med * cr

        # dp[j][i]: min cost using j windows entirely within nums[0..i-1]
        prev = [0] * (n + 1)  # j = 0
        for j in range(1, k + 1):
            cur = [INF] * (n + 1)
            for i in range(1, n + 1):
                best = cur[i - 1]
                if i >= x and prev[i - x] != INF:
                    c = prev[i - x] + cost[i - x]
                    if c < best:
                        best = c
                cur[i] = best
            prev = cur
        return int(prev[n])
