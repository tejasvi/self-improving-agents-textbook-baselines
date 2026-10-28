from typing import List


class Solution:
    def maxValue(self, nums: List[int], k: int) -> int:
        n = len(nums)

        def sweep(order):
            # dp[j] = set of OR values achievable by choosing j elements so far
            dp = [set() for _ in range(k + 1)]
            dp[0] = {0}
            seq = []
            for idx in order:
                x = nums[idx]
                for j in range(k, 0, -1):
                    if dp[j - 1]:
                        dp[j].update(v | x for v in dp[j - 1])
                seq.append(frozenset(dp[k]))
            return seq

        # pre[i]: OR-values from choosing k elements among nums[:i+1]
        pre = sweep(range(n))
        # suf[i]: OR-values from choosing k elements among nums[n-1-i:]
        suf = sweep(range(n - 1, -1, -1))

        best = 0
        for m in range(k, n - k + 1):
            # left part from nums[:m], right part from nums[m:]
            L = pre[m - 1]
            R = suf[n - 1 - m]
            for a in L:
                for b in R:
                    if a ^ b > best:
                        best = a ^ b
        return best
