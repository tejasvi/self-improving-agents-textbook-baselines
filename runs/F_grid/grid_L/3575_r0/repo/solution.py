from typing import List


class Solution:
    def maxValue(self, nums: List[int], k: int) -> int:
        n = len(nums)

        # pre[m]: set of OR values from choosing exactly k elements of nums[:m]
        pre = [None] * (n + 1)
        dp = [set() for _ in range(k + 1)]
        dp[0] = {0}
        pre[0] = set()
        for i, x in enumerate(nums):
            for j in range(min(i + 1, k), 0, -1):
                if dp[j - 1]:
                    dp[j] |= {v | x for v in dp[j - 1]}
            pre[i + 1] = set(dp[k])

        # suf[m]: set of OR values from choosing exactly k elements of nums[m:]
        suf = [None] * (n + 1)
        dp = [set() for _ in range(k + 1)]
        dp[0] = {0}
        suf[n] = set()
        for i in range(n - 1, -1, -1):
            x = nums[i]
            for j in range(min(n - i, k), 0, -1):
                if dp[j - 1]:
                    dp[j] |= {v | x for v in dp[j - 1]}
            suf[i] = set(dp[k])

        best = 0
        for m in range(k, n - k + 1):
            L = pre[m]
            R = suf[m]
            for a in L:
                for b in R:
                    if a ^ b > best:
                        best = a ^ b
        return best
