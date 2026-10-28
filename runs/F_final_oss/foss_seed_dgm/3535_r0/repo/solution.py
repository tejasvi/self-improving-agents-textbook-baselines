from typing import List

MOD = 10**9 + 7

class Solution:
    def countOfPairs(self, nums: List[int]) -> int:
        n = len(nums)
        max_val = max(nums)
        # dp for current position, size max_val+1
        dp = [0] * (max_val + 1)
        # initialize for first element
        for v in range(nums[0] + 1):
            dp[v] = 1
        # iterate through positions
        for i in range(n - 1):
            delta = max(0, nums[i + 1] - nums[i])
            # prefix sums of dp
            pref = [0] * (max_val + 1)
            running = 0
            for v in range(max_val + 1):
                running = (running + dp[v]) % MOD
                pref[v] = running
            # new dp for i+1
            new_dp = [0] * (max_val + 1)
            # possible values for a_{i+1} are 0..nums[i+1]
            for v_next in range(nums[i + 1] + 1):
                max_prev = v_next - delta
                if max_prev >= 0:
                    new_dp[v_next] = pref[max_prev]
                # else remain 0
            dp = new_dp
        # result is sum of ways for last position values within its bound
        result = sum(dp[v] for v in range(nums[-1] + 1)) % MOD
        return result
