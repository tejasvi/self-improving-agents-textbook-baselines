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
            m = 0
            for k in range(g, M + 1, g):
                m += cnt[k]
            pairs = m * (m - 1) // 2
            for k in range(2 * g, M + 1, g):
                pairs -= exact[k]
            exact[g] = pairs

        # prefix counts over sorted gcd values
        prefix = []  # prefix[i] = number of pairs with gcd <= value at index
        values = []
        total = 0
        for g in range(1, M + 1):
            if exact[g]:
                total += exact[g]
                values.append(g)
                prefix.append(total)

        res = []
        for q in queries:
            # smallest idx with prefix[idx] > q
            idx = bisect_right(prefix, q)
            res.append(values[idx])
        return res
