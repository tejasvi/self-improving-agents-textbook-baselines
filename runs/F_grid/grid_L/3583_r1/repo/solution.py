from typing import List
from bisect import bisect_right


class Solution:
    def gcdValues(self, nums: List[int], queries: List[int]) -> List[int]:
        if not nums:
            return []
        M = max(nums)
        cnt = [0] * (M + 1)
        for x in nums:
            cnt[x] += 1

        # exact[g] = number of pairs (i<j) with gcd exactly g
        exact = [0] * (M + 1)
        for g in range(M, 0, -1):
            m = sum(cnt[g::g])
            total = m * (m - 1) // 2
            for k in range(2 * g, M + 1, g):
                total -= exact[k]
            exact[g] = total

        # prefix sums: prefix[i] = number of pairs with gcd <= g_i
        gs = []
        prefix = []
        running = 0
        for g in range(1, M + 1):
            if exact[g]:
                running += exact[g]
                gs.append(g)
                prefix.append(running)

        ans = []
        for q in queries:
            idx = bisect_right(prefix, q)
            ans.append(gs[idx])
        return ans
