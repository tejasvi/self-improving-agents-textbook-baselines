from typing import List
import math

MOD = 10**9 + 7

class Solution:
    def subsequencePairCount(self, nums: List[int]) -> int:
        """Return number of ordered pairs of non‑empty disjoint subsequences
        whose GCDs are equal, modulo 1e9+7.
        """
        if not nums:
            return 0
        max_val = max(nums)
        size = max_val + 1  # include 0 for empty subsequence indicator
        # dp[g1][g2] = number of ways for processed prefix
        dp = [[0] * size for _ in range(size)]
        dp[0][0] = 1  # both subsequences empty initially
        for x in nums:
            ndp = [[0] * size for _ in range(size)]
            for g1 in range(size):
                row = dp[g1]
                for g2 in range(size):
                    cur = row[g2]
                    if cur == 0:
                        continue
                    # option 1: skip element
                    ndp[g1][g2] = (ndp[g1][g2] + cur) % MOD
                    # option 2: put in subsequence 1
                    ng1 = x if g1 == 0 else math.gcd(g1, x)
                    ndp[ng1][g2] = (ndp[ng1][g2] + cur) % MOD
                    # option 3: put in subsequence 2
                    ng2 = x if g2 == 0 else math.gcd(g2, x)
                    ndp[g1][ng2] = (ndp[g1][ng2] + cur) % MOD
            dp = ndp
        # sum over states where both GCDs are equal and non‑zero
        ans = 0
        for g in range(1, size):
            ans = (ans + dp[g][g]) % MOD
        return ans
