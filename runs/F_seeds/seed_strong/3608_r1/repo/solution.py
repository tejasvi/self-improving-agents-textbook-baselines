from math import gcd
from operator import add
from typing import *

MOD = 10**9 + 7

class Solution:
    def subsequencePairCount(self, nums: List[int]) -> int:
        M = 201
        # dp[a][b]: ways to assign processed elements to seq1 (gcd a), seq2 (gcd b),
        # or neither; 0 denotes empty sequence. Table is kept symmetric.
        dp = [[0] * M for _ in range(M)]
        dp[0][0] = 1
        for x in nums:
            gx = [gcd(a, x) for a in range(M)]
            # T[t][b] = sum over a with gcd(a,x)=t of dp[a][b]  (add x to seq1)
            T = [[0] * M for _ in range(M)]
            for a in range(M):
                row = dp[a]
                if any(row):
                    t = gx[a]
                    T[t] = list(map(add, T[t], row))
            TT = [list(r) for r in zip(*T)]  # add x to seq2
            new = [
                [(p + q + r) % MOD for p, q, r in zip(dp[i], T[i], TT[i])]
                for i in range(M)
            ]
            dp = new
        ans = 0
        for a in range(1, M):
            ans += dp[a][a]
        return ans % MOD
