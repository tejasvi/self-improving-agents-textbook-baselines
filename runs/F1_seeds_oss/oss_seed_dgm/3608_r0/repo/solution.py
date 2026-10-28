from typing import List
import math

MOD = 10**9 + 7

class Solution:
    def subsequencePairCount(self, nums: List[int]) -> int:
        """Return the number of ordered pairs of non‑empty disjoint subsequences
        whose GCDs are equal.
        
        We treat each element of ``nums`` independently and decide whether it
        belongs to the first subsequence, the second subsequence, or to neither.
        The state of a DP consists of the current GCD of the first subsequence
        (or 0 if it is still empty) and the current GCD of the second subsequence
        (or 0 if empty).  For each number we update the DP with the three
        possibilities.  The total number of states is at most (max_val+1)^2
        where ``max_val`` ≤ 200, i.e. 40 401, which is easily fast enough for
        ``len(nums) ≤ 200``.
        """
        if not nums:
            return 0
        max_val = max(nums)
        # dp[g1][g2] – number of ways after processing some prefix where
        #   gcd of seq1 is g1 (0 means empty) and gcd of seq2 is g2 (0 means empty)
        dp = [[0] * (max_val + 1) for _ in range(max_val + 1)]
        dp[0][0] = 1  # nothing chosen yet
        for a in nums:
            new_dp = [[0] * (max_val + 1) for _ in range(max_val + 1)]
            for g1 in range(max_val + 1):
                row = dp[g1]
                for g2 in range(max_val + 1):
                    cur = row[g2]
                    if cur == 0:
                        continue
                    # 1) ignore a
                    new_dp[g1][g2] = (new_dp[g1][g2] + cur) % MOD
                    # 2) put a into the first subsequence
                    ng1 = a if g1 == 0 else math.gcd(g1, a)
                    new_dp[ng1][g2] = (new_dp[ng1][g2] + cur) % MOD
                    # 3) put a into the second subsequence
                    ng2 = a if g2 == 0 else math.gcd(g2, a)
                    new_dp[g1][ng2] = (new_dp[g1][ng2] + cur) % MOD
            dp = new_dp
        # Both subsequences must be non‑empty, i.e. gcd > 0, and equal.
        ans = 0
        for g in range(1, max_val + 1):
            ans = (ans + dp[g][g]) % MOD
        return ans
