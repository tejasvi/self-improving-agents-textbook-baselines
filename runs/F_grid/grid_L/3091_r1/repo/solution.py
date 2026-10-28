from typing import List
from collections import Counter


class Solution:
    def countSubMultisets(self, nums: List[int], l: int, r: int) -> int:
        MOD = 10**9 + 7
        cnt = Counter(nums)
        zeros = cnt.pop(0, 0)
        S = sum(v * c for v, c in cnt.items())
        dp = [0] * (S + 1)
        dp[0] = 1
        for v, c in cnt.items():
            if v > S:
                continue
            new = [0] * (S + 1)
            shift = (c + 1) * v
            for s in range(S + 1):
                val = dp[s]
                if s >= v:
                    val += new[s - v]
                if s >= shift:
                    val -= dp[s - shift]
                new[s] = val % MOD
            dp = new
        total = sum(dp[l:min(r, S) + 1]) if l <= S else 0
        return total % MOD * (zeros + 1) % MOD
