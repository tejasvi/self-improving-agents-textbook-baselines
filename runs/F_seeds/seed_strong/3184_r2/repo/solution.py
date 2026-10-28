from typing import *


class Solution:
    def maxBalancedSubsequenceSum(self, nums: List[int]) -> int:
        n = len(nums)
        keys = [nums[i] - i for i in range(n)]
        sorted_keys = sorted(set(keys))
        rank = {v: i + 1 for i, v in enumerate(sorted_keys)}
        m = len(sorted_keys)
        tree = [None] * (m + 1)  # Fenwick tree for prefix max, None = -inf

        def update(pos, val):
            while pos <= m:
                if tree[pos] is None or tree[pos] < val:
                    tree[pos] = val
                pos += pos & (-pos)

        def query(pos):
            best = None
            while pos > 0:
                t = tree[pos]
                if t is not None and (best is None or t > best):
                    best = t
                pos -= pos & (-pos)
            return best

        ans = None
        for i in range(n):
            r = rank[keys[i]]
            best = query(r)
            dp = nums[i] + (best if best is not None and best > 0 else 0)
            update(r, dp)
            if ans is None or dp > ans:
                ans = dp
        return ans
