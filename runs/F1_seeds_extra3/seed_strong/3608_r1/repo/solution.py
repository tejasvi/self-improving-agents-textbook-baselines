from typing import *
from math import gcd


class Solution:
    def subsequencePairCount(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        M = max(nums) if nums else 1
        N = M + 1
        # dp[a][b]: number of ways (over processed elements) that seq1 has gcd a
        # and seq2 has gcd b, with 0 meaning empty. Kept symmetric.
        dp = [[0] * N for _ in range(N)]
        dp[0][0] = 1
        for x in nums:
            # A[t][b] += dp[a][b] where t = gcd(a, x): x added to seq1
            A = [[0] * N for _ in range(N)]
            for a in range(N):
                row = dp[a]
                if not any(row):
                    continue
                t = gcd(a, x)
                cur = A[t]
                A[t] = [p + q for p, q in zip(cur, row)]
            AT = [list(col) for col in zip(*A)]
            dp = [
                [(d + s + u) % MOD for d, s, u in zip(dr, ar, atr)]
                for dr, ar, atr in zip(dp, A, AT)
            ]
        return sum(dp[a][a] for a in range(1, N)) % MOD
