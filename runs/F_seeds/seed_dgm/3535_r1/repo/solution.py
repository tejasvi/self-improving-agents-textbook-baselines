from typing import List


class Solution:
    def countOfPairs(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        # dp[v]: number of valid prefixes with arr1[i] == v
        prev = [1] * (nums[0] + 1)
        for i in range(1, n):
            cur_max = nums[i]
            d = max(0, nums[i] - nums[i - 1])
            # prefix sums of prev
            pref = [0] * (len(prev) + 1)
            for v, c in enumerate(prev):
                pref[v + 1] = (pref[v] + c) % MOD
            cur = [0] * (cur_max + 1)
            for w in range(cur_max + 1):
                # need v + d <= w and v <= len(prev)-1
                hi = w - d
                if hi < 0:
                    cur[w] = 0
                    continue
                hi = min(hi, len(prev) - 1)
                cur[w] = pref[hi + 1]
            prev = cur
        return sum(prev) % MOD
