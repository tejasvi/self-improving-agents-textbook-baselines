from typing import List


class Solution:
    def sumOfPowers(self, nums: List[int], k: int) -> int:
        MOD = 10**9 + 7
        a = sorted(nums)
        n = len(a)

        # Candidate minimum differences: all pairwise differences of sorted array.
        cand = sorted({a[j] - a[i] for i in range(n) for j in range(i + 1, n)})

        def count_at_least(v: int) -> int:
            """Number of k-subsets whose adjacent (sorted) gaps are all >= v."""
            if v == 0:
                from math import comb
                return comb(n, k) % MOD
            # bound[i]: number of indices p with a[p] <= a[i] - v (valid predecessors of i)
            bound = [0] * n
            p = 0
            for i in range(n):
                while p < n and a[p] <= a[i] - v:
                    p += 1
                bound[i] = p
            # dp[i] = ways to choose current size elements ending at i
            dp = [1] * n
            for _ in range(k - 1):
                # prefix sums of dp
                pre = [0] * (n + 1)
                for i in range(n):
                    pre[i + 1] = (pre[i] + dp[i]) % MOD
                dp = [pre[bound[i]] for i in range(n)]
            return sum(dp) % MOD

        total = 0
        m = len(cand)
        G = [count_at_least(v) for v in cand]
        for t in range(m):
            nxt = G[t + 1] if t + 1 < m else 0
            total = (total + cand[t] % MOD * ((G[t] - nxt) % MOD)) % MOD
        return total % MOD
