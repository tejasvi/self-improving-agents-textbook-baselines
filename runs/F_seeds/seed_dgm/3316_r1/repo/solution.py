from bisect import bisect_right
from typing import List


class Solution:
    def sumOfPowers(self, nums: List[int], k: int) -> int:
        MOD = 10 ** 9 + 7
        a = sorted(nums)
        n = len(a)

        # distinct pairwise differences
        diffs = sorted({a[j] - a[i] for i in range(n) for j in range(i + 1, n)})

        def count_at_least(d: int) -> int:
            # number of k-subsequences where every adjacent gap (in sorted order) >= d
            # p[j] = number of indices i < j with a[j] - a[i] >= d (valid i form a prefix)
            p = [min(j, bisect_right(a, a[j] - d)) for j in range(n)]
            dp = [1] * n  # ways with c = 1 chosen, ending at j
            for _ in range(k - 1):
                prefix = [0] * (n + 1)
                for j in range(n):
                    prefix[j + 1] = (prefix[j] + dp[j]) % MOD
                dp = [prefix[p[j]] for j in range(n)]
            return sum(dp) % MOD

        m = len(diffs)
        g = [count_at_least(d) for d in diffs]
        g.append(0)  # no subsequence has min gap >= infinity
        ans = 0
        for idx in range(m):
            exact = (g[idx] - g[idx + 1]) % MOD
            ans = (ans + diffs[idx] % MOD * exact) % MOD
        return ans
