from typing import List
import math

MOD = 10**9 + 7

class Solution:
    def subsequencePairCount(self, nums: List[int]) -> int:
        # DP over possible GCDs of the two disjoint subsequences.
        # dp[g1][g2] = number of ways to assign processed elements such that
        #   subsequence1 (if non‑empty) has GCD g1, otherwise g1 == 0;
        #   subsequence2 (if non‑empty) has GCD g2, otherwise g2 == 0.
        max_val = max(nums) if nums else 0
        size = max_val + 1
        # initialize dp with both empty
        dp = [[0] * size for _ in range(size)]
        dp[0][0] = 1
        for x in nums:
            ndp = [[0] * size for _ in range(size)]
            for g1 in range(size):
                row = dp[g1]
                for g2 in range(size):
                    cur = row[g2]
                    if cur == 0:
                        continue
                    # option 1: put x in neither subsequence
                    ndp[g1][g2] = (ndp[g1][g2] + cur) % MOD
                    # option 2: put x in subsequence1
                    ng1 = x if g1 == 0 else math.gcd(g1, x)
                    ndp[ng1][g2] = (ndp[ng1][g2] + cur) % MOD
                    # option 3: put x in subsequence2
                    ng2 = x if g2 == 0 else math.gcd(g2, x)
                    ndp[g1][ng2] = (ndp[g1][ng2] + cur) % MOD
            dp = ndp
        # sum over states where both subsequences are non‑empty (g>0) and GCD equal
        ans = 0
        for g in range(1, size):
            ans = (ans + dp[g][g]) % MOD
        return ans
