from typing import List
from collections import Counter


class Solution:
    def countSubMultisets(self, nums: List[int], l: int, r: int) -> int:
        MOD = 10**9 + 7
        cnt = Counter(nums)
        zeros = cnt.pop(0, 0)
        S = sum(v * c for v, c in cnt.items())
        if l > S:
            return 0
        dp = [0] * (S + 1)
        dp[0] = 1
        for v, c in cnt.items():
            # P[s] = sum_{k>=0} dp[s - k*v]
            P = [0] * (S + 1)
            for s in range(S + 1):
                P[s] = (dp[s] + (P[s - v] if s >= v else 0)) % MOD
            step = (c + 1) * v
            new = [0] * (S + 1)
            for s in range(S + 1):
                new[s] = (P[s] - (P[s - step] if s >= step else 0)) % MOD
            dp = new
        total = sum(dp[l:min(r, S) + 1]) % MOD if l <= S else 0
        return total * (zeros + 1) % MOD
