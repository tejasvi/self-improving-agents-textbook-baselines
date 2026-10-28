from typing import List


class Solution:
    def countOfPairs(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        # dp[v] = number of valid prefixes ending with arr1[i] == v
        prev = [1] * (nums[0] + 1)
        for i in range(1, n):
            cur_max = nums[i]
            d = max(0, nums[i] - nums[i - 1])
            # prefix sums of prev
            pref = [0] * (len(prev) + 1)
            for j, x in enumerate(prev):
                pref[j + 1] = (pref[j] + x) % MOD
            cur = [0] * (cur_max + 1)
            for v in range(cur_max + 1):
                # need prev_v <= v - d, prev_v in [0, min(len(prev)-1, v-d)]
                hi = min(len(prev) - 1, v - d)
                if hi >= 0:
                    cur[v] = pref[hi + 1]
            prev = cur
        return sum(prev) % MOD
