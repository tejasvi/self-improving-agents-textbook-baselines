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
                pos += pos & (-pos)

        def query(pos):
            best = NEG
            while pos > 0:
                if tree[pos] > best:
                    best = tree[pos]
                pos -= pos & (-pos)
            return best

        ans = None
        for j in range(n):
            r = rank[keys[j]]
            prev = query(r)
            cur = nums[j] + (prev if prev > 0 else 0)
            update(r, cur)
            if ans is None or cur > ans:
                ans = cur
        return ans
