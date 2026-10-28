from typing import List
from math import gcd

MOD = 10**9 + 7
MAX_VAL = 200  # as per constraints

class Solution:
    def subsequencePairCount(self, nums: List[int]) -> int:
        """Return number of ordered pairs of non‑empty disjoint subsequences
        whose GCDs are equal.
        """
        # dp[a][b] = number of ways after processing some prefix where
        #   GCD of seq1 is a (0 means seq1 empty) and GCD of seq2 is b (0 means empty).
        dp = [[0] * (MAX_VAL + 1) for _ in range(MAX_VAL + 1)]
        dp[0][0] = 1  # both empty before processing any element

        for x in nums:
            # start from current dp, create a fresh copy for the next step.
            ndp = [row[:] for row in dp]
            for a in range(MAX_VAL + 1):
                for b in range(MAX_VAL + 1):
                    cur = dp[a][b]
                    if cur == 0:
                        continue
                    # put x into seq1 (seq2 unchanged)
                    na = x if a == 0 else gcd(a, x)
                    ndp[na][b] = (ndp[na][b] + cur) % MOD
                    # put x into seq2 (seq1 unchanged)
                    nb = x if b == 0 else gcd(b, x)
                    ndp[a][nb] = (ndp[a][nb] + cur) % MOD
                    # leaving x unused is already represented by copying dp to ndp
            dp = ndp

        # sum over states where both subsequences are non‑empty (gcd > 0) and equal.
        ans = 0
        for g in range(1, MAX_VAL + 1):
            ans = (ans + dp[g][g]) % MOD
        return ans
