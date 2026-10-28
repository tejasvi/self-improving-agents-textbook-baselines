from typing import List

MOD = 10**9 + 7

class Solution:
    def countOfPairs(self, nums: List[int]) -> int:
        n = len(nums)
        max_num = max(nums)
        # dp stores ways for previous index, indexed by possible a value (0..max_num)
        dp_prev = [0] * (max_num + 1)
        # initialize for i=0: any a[0] between 0 and nums[0]
        for v in range(nums[0] + 1):
            dp_prev[v] = 1
        # process rest positions
        for i in range(1, n):
            # minimal required increase from a[i-1] to a[i]
            delta = max(0, nums[i] - nums[i-1])
            # prefix sums of dp_prev for quick range sum
            prefix = [0] * (max_num + 2)
            for v in range(max_num + 1):
                prefix[v+1] = (prefix[v] + dp_prev[v]) % MOD
            dp_cur = [0] * (max_num + 1)
            for v in range(nums[i] + 1):  # a[i] can be at most nums[i]
                # allowed previous a[i-1] must satisfy a[i-1] <= v - delta
                limit = v - delta
                if limit < 0:
                    dp_cur[v] = 0
                else:
                    hi = min(limit, nums[i-1])  # previous a cannot exceed nums[i-1]
                    dp_cur[v] = prefix[hi+1]  # sum_{u=0..hi} dp_prev[u]
            dp_prev = dp_cur
        # answer is sum of ways for last position over all valid a[n-1]
        ans = sum(dp_prev[v] for v in range(nums[-1] + 1)) % MOD
        return ans
