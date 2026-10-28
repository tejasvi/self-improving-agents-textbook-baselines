from typing import List
from math import gcd


class Solution:
    def subsequencePairCount(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        M = max(nums) if nums else 0
        # dp[a][b]: ways where gcd of seq1 is a, gcd of seq2 is b (0 = empty)
        dp = [[0] * (M + 1) for _ in range(M + 1)]
        dp[0][0] = 1
        for x in nums:
            new = [row[:] for row in dp]  # skip x
            for a in range(M + 1):
                row = dp[a]
                for b in range(M + 1):
                    v = row[b]
                    if not v:
                        continue
                    ga = gcd(a, x)
                    new[ga][b] = (new[ga][b] + v) % MOD
                    gb = gcd(b, x)
                    new[a][gb] = (new[a][gb] + v) % MOD
            dp = new
        ans = 0
        for g in range(1, M + 1):
            ans += dp[g][g]
        return ans % MOD
