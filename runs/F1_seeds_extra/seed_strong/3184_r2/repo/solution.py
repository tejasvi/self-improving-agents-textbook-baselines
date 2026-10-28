from typing import *


class Solution:
    def maxBalancedSubsequenceSum(self, nums: List[int]) -> int:
        n = len(nums)
        keys = [nums[i] - i for i in range(n)]
        sorted_keys = sorted(set(keys))
        rank = {k: r + 1 for r, k in enumerate(sorted_keys)}
        m = len(sorted_keys)
        NEG = float("-inf")
        tree = [NEG] * (m + 1)

        def update(pos, val):
            while pos <= m:
                if tree[pos] < val:
                    tree[pos] = val
                pos += pos & -pos

        def query(pos):
            res = NEG
            while pos > 0:
                if tree[pos] > res:
                    res = tree[pos]
                pos -= pos & -pos
            return res

        best = NEG
        for i in range(n):
            r = rank[keys[i]]
            prev = query(r)  # max dp[j] with nums[j]-j <= nums[i]-i
            dp = nums[i] + (prev if prev > 0 else 0)
            update(r, dp)
            if dp > best:
                best = dp
        return int(best)
