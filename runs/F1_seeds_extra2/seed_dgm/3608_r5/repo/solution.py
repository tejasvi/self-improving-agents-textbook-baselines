from math import gcd
from typing import List


class Solution:
    def subsequencePairCount(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        M = max(nums)
        # dp[a][b]: number of ways to split processed elements into
        # seq1 (gcd a) and seq2 (gcd b), others unused; 0 means empty.
        dp = [[0] * (M + 1) for _ in range(M + 1)]
        dp[0][0] = 1
        for x in nums:
            new = [row[:] for row in dp]
            for a in range(M + 1):
                row = dp[a]
                for b in range(M + 1):
                    v = row[b]
                    if not v:
                        continue
                    na = gcd(a, x)
                    new[na][b] = (new[na][b] + v) % MOD
                    nb = gcd(b, x)
                    new[a][nb] = (new[a][nb] + v) % MOD
            dp = new
        ans = 0
        for g in range(1, M + 1):
            ans += dp[g][g]
        return ans % MOD
