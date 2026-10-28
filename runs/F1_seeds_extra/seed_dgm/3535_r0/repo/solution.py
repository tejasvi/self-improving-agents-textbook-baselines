from typing import List


class Solution:
    def countOfPairs(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        # dp[a] = number of valid prefixes where arr1[i] == a
        prev = [1] * (nums[0] + 1)
        for i in range(1, n):
            d = max(0, nums[i] - nums[i - 1])
            # prefix sums of prev
            pref = []
            s = 0
            for v in prev:
                s = (s + v) % MOD
                pref.append(s)
            cur = [0] * (nums[i] + 1)
            for b in range(nums[i] + 1):
                up = b - d
                if up >= 0:
                    cur[b] = pref[min(up, len(prev) - 1)]
            prev = cur
        return sum(prev) % MOD
