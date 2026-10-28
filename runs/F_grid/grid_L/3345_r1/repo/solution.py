from typing import List


class Solution:
    def sumOfPower(self, nums: List[int], k: int) -> int:
        MOD = 10**9 + 7
        # dp[s] = sum over subsets T of processed elements with sum s,
        # of 2^(number of processed elements not in T).
        dp = [0] * (k + 1)
        dp[0] = 1
        for x in nums:
            new = [(v * 2) % MOD for v in dp]  # element not chosen
            if x <= k:
                for s in range(x, k + 1):  # element chosen
                    new[s] = (new[s] + dp[s - x]) % MOD
            dp = new
        return dp[k] % MOD
