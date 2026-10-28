from typing import List


class Solution:
    def maxValue(self, nums: List[int], k: int) -> int:
        n = len(nums)

        def prefix_sets(arr):
            # res[m] = set of OR values achievable by choosing exactly k
            # elements from arr[:m]
            dp = [set() for _ in range(k + 1)]
            dp[0].add(0)
            res = [set() for _ in range(n + 1)]
            for i, x in enumerate(arr):
                for c in range(min(k, i + 1), 0, -1):
                    if dp[c - 1]:
                        dp[c].update({v | x for v in dp[c - 1]})
                res[i + 1] = set(dp[k])
            return res

        left = prefix_sets(nums)
        right = prefix_sets(nums[::-1])  # right[m] covers nums[n-m:]

        best = 0
        for m in range(k, n - k + 1):
            L = left[m]
            R = right[n - m]
            for a in L:
                for b in R:
                    if a ^ b > best:
                        best = a ^ b
        return best
