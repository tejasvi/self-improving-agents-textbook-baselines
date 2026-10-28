from typing import List


class Solution:
    def maxValue(self, nums: List[int], k: int) -> int:
        n = len(nums)

        def sweep(seq):
            # res[i] = set of OR values achievable by choosing exactly k
            # elements from seq[:i]
            res = [None] * (n + 1)
            dp = [set() for _ in range(k + 1)]
            dp[0].add(0)
            for i, x in enumerate(seq):
                res[i] = frozenset(dp[k])
                for j in range(k, 0, -1):
                    if dp[j - 1]:
                        dp[j].update(v | x for v in dp[j - 1])
            res[n] = frozenset(dp[k])
            return res

        pre = sweep(nums)
        suf = sweep(nums[::-1])  # suf[j] covers nums[n-j:]

        best = 0
        for m in range(k, n - k + 1):
            left = pre[m]
            right = suf[n - m]
            for a in left:
                for b in right:
                    if a ^ b > best:
                        best = a ^ b
        return best
