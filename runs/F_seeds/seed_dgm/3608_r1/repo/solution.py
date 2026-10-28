from math import gcd
from typing import List


class Solution:
    def subsequencePairCount(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        M = max(nums) if nums else 0
        # dp[a][b]: number of ways (over processed elements) to split a subset
        # into seq1 with gcd a and seq2 with gcd b (0 means empty).
        dp = [[0] * (M + 1) for _ in range(M + 1)]
        dp[0][0] = 1
        for x in nums:
            new = [row[:] for row in dp]  # element not used
            for a in range(M + 1):
                row = dp[a]
                for b in range(M + 1):
                    c = row[b]
                    if not c:
                        continue
                    ga = gcd(a, x)
                    new[ga][b] = (new[ga][b] + c) % MOD
                    gb = gcd(b, x)
                    new[a][gb] = (new[a][gb] + c) % MOD
            dp = new
        ans = 0
        for g in range(1, M + 1):
            ans += dp[g][g]
        return ans % MOD
