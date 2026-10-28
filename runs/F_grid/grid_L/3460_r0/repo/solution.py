from typing import List


class Solution:
    def numberOfPermutations(self, n: int, requirements: List[List[int]]) -> int:
        MOD = 10 ** 9 + 7
        req = {}
        for end, cnt in requirements:
            req[end] = cnt
        K = max(req.values())  # prefix inversion counts are nondecreasing
        # dp[k]: ways to have k inversions in prefix of length i (processed so far)
        dp = [0] * (K + 1)
        dp[0] = 1  # empty prefix
        for i in range(n):
            # choose c in [0, i] new inversions at position i
            # new[k] = sum_{c=0..i} dp[k-c]  via prefix sums
            pref = [0] * (K + 2)
            for k in range(K + 1):
                pref[k + 1] = (pref[k] + dp[k]) % MOD
            new = [0] * (K + 1)
            for k in range(K + 1):
                lo = max(0, k - i)
                new[k] = (pref[k + 1] - pref[lo]) % MOD
            if i in req:
                t = req[i]
                for k in range(K + 1):
                    if k != t:
                        new[k] = 0
            dp = new
        return dp[req[n - 1]] % MOD
