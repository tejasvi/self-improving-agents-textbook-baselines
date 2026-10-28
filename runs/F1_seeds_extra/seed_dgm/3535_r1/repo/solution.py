from typing import List


class Solution:
    def countOfPairs(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        # dp[a] = number of valid prefixes where arr1[i] == a
        prev = [1] * (nums[0] + 1)
        for i in range(1, n):
            cur_max = nums[i]
            shift = max(0, nums[i] - nums[i - 1])
            # prefix sums of prev
            pref = [0] * (len(prev) + 1)
            for j, v in enumerate(prev):
                pref[j + 1] = (pref[j] + v) % MOD
            cur = [0] * (cur_max + 1)
            for a2 in range(cur_max + 1):
                # need a + shift <= a2, a in [0, len(prev)-1]
                hi = min(a2 - shift, len(prev) - 1)
                if hi >= 0:
                    cur[a2] = pref[hi + 1]
            prev = cur
        return sum(prev) % MOD
