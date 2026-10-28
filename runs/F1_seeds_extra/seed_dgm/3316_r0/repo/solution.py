from bisect import bisect_right
from typing import List


class Solution:
    def sumOfPowers(self, nums: List[int], k: int) -> int:
        MOD = 10**9 + 7
        a = sorted(nums)
        n = len(a)

        # Candidate values for the minimum difference: all pairwise differences.
        cands = sorted({a[j] - a[i] for i in range(n) for j in range(i + 1, n)})
        if not cands:
            return 0

        def count_at_least(d: int) -> int:
            # dp[i] = number of ways to choose j elements ending at index i,
            # with all adjacent differences >= d.
            dp = [1] * n
            pos = [bisect_right(a, a[i] - d) for i in range(n)]
            for _ in range(k - 1):
                prefix = [0] * (n + 1)
                for i in range(n):
                    prefix[i + 1] = (prefix[i] + dp[i]) % MOD
                new = [0] * n
                for i in range(n):
                    t = min(pos[i], i)
                    new[i] = prefix[t]
                dp = new
            return sum(dp) % MOD

        total = 0
        m = len(cands)
        vals = [count_at_least(d) for d in cands]
        for idx in range(m):
            nxt = vals[idx + 1] if idx + 1 < m else 0
            total = (total + cands[idx] * (vals[idx] - nxt)) % MOD
        return total % MOD
