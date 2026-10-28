from typing import List


class Solution:
    def numberOfPermutations(self, n: int, requirements: List[List[int]]) -> int:
        MOD = 10**9 + 7
        K = 401  # max cnt is 400; inversion counts never decrease with prefix length
        req = {}
        for end, cnt in requirements:
            req[end] = cnt

        # dp[k]: number of arrangements of prefix of length i+1 with exactly k inversions
        dp = [0] * K
        dp[0] = 1
        if 0 in req:
            if req[0] != 0:
                return 0
        for i in range(1, n):
            # prefix sums of dp
            P = [0] * (K + 1)
            for k in range(K):
                P[k + 1] = (P[k] + dp[k]) % MOD
            new = [0] * K
            for k in range(K):
                lo = k - i  # sum dp[lo..k]
                s = P[k + 1] - (P[lo] if lo > 0 else 0)
                new[k] = s % MOD
            if i in req:
                t = req[i]
                val = new[t] if t < K else 0
                new = [0] * K
                new[t] = val
            dp = new
        return sum(dp) % MOD
