from typing import List


class Solution:
    def countOfPairs(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        # dp[v] = number of valid prefixes where arr1[i] == v
        n = len(nums)
        dp = [0] * (nums[0] + 1)
        for v in range(nums[0] + 1):
            dp[v] = 1
        for i in range(1, n):
            prev = dp
            # prefix sums of prev
            pre = [0] * (len(prev) + 1)
            for v, c in enumerate(prev):
                pre[v + 1] = (pre[v] + c) % MOD
            d = nums[i] - nums[i - 1]
            cur = [0] * (nums[i] + 1)
            for w in range(nums[i] + 1):
                # need v + max(0, d) <= w, v <= len(prev)-1
                hi = min(w - max(0, d), len(prev) - 1)
                if hi >= 0:
                    cur[w] = pre[hi + 1]
            dp = cur
        return sum(dp) % MOD
