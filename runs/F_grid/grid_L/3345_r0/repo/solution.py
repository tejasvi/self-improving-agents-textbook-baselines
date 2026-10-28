from typing import List


class Solution:
    def sumOfPower(self, nums: List[int], k: int) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        # dp[c][s]: number of subsets of size c with sum s (s <= k only)
        dp = [[0] * (k + 1) for _ in range(n + 1)]
        dp[0][0] = 1
        for x in nums:
            if x > k:
                continue
            for c in range(n, 0, -1):
                prev = dp[c - 1]
                cur = dp[c]
                for s in range(k, x - 1, -1):
                    if prev[s - x]:
                        cur[s] = (cur[s] + prev[s - x]) % MOD
        # Each subset S with sum k is contained in 2^(n-|S|) subsequences,
        # and each such subsequence contributes one matching subset.
        pow2 = [1] * (n + 1)
        for i in range(1, n + 1):
            pow2[i] = pow2[i - 1] * 2 % MOD
        ans = 0
        for c in range(n + 1):
            ans = (ans + dp[c][k] * pow2[n - c]) % MOD
        return ans
