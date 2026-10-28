from typing import *


class Solution:
    def maxBalancedSubsequenceSum(self, nums: List[int]) -> int:
        n = len(nums)
        b = [nums[i] - i for i in range(n)]
        vals = sorted(set(b))
        rank = {v: k + 1 for k, v in enumerate(vals)}
        m = len(vals)
        NEG = float('-inf')
        tree = [NEG] * (m + 1)

        def update(p, v):
            while p <= m:
                if tree[p] < v:
                    tree[p] = v
                p += p & -p

        def query(p):
            res = 0  # starting fresh is always allowed
            while p > 0:
                if tree[p] > res:
                    res = tree[p]
                p -= p & -p
            return res

        best = None
        for i in range(n):
            r = rank[b[i]]
            dp = nums[i] + query(r)
            update(r, dp)
            if best is None or dp > best:
                best = dp
        return best
