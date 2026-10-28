from typing import List

MOD = 10**9 + 7

class Solution:
    def countOfPairs(self, nums: List[int]) -> int:
        # DP over possible values of arr1 at each position.
        # arr1[i] must be in [0, nums[i]] and must satisfy
        # arr1[i+1] - arr1[i] >= max(0, nums[i+1] - nums[i])
        n = len(nums)
        if n == 0:
            return 0
        max_val = max(nums)
        # dp[v] = number of ways where current arr1 value is v
        dp = [0] * (max_val + 1)
        for v in range(nums[0] + 1):
            dp[v] = 1
        for i in range(n - 1):
            delta = max(0, nums[i + 1] - nums[i])
            # prefix sums of dp for quick range sum
            prefix = [0] * (max_val + 2)
            for v in range(max_val + 1):
                prefix[v + 1] = (prefix[v] + dp[v]) % MOD
            new_dp = [0] * (max_val + 1)
            # for each possible next value v2 within [0, nums[i+1]]
            for v2 in range(nums[i + 1] + 1):
                # we need previous v such that v <= v2 - delta
                max_prev = v2 - delta
                if max_prev < 0:
                    continue
                # sum dp[v] for v in [0, max_prev]
                new_dp[v2] = prefix[max_prev + 1]
            dp = new_dp
        # answer is sum over last dp values within allowed range
        return sum(dp[v] for v in range(nums[-1] + 1)) % MOD
