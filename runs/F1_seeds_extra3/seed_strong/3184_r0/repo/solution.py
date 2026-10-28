from typing import *


class Solution:
    def maxBalancedSubsequenceSum(self, nums: List[int]) -> int:
        n = len(nums)
        keys = [nums[i] - i for i in range(n)]
        uniq = sorted(set(keys))
        rank = {v: idx + 1 for idx, v in enumerate(uniq)}
        m = len(uniq)
        NEG = float("-inf")
        tree = [NEG] * (m + 1)

        def update(pos, val):
            while pos <= m:
                if tree[pos] < val:
                    tree[pos] = val
                pos += pos & -pos

        def query(pos):
            best = NEG
            while pos > 0:
                if tree[pos] > best:
                    best = tree[pos]
                pos -= pos & -pos
            return best

        ans = NEG
        for i in range(n):
            r = rank[keys[i]]
            prev = query(r)
            dp = nums[i] + (prev if prev > 0 else 0)
            update(r, dp)
            if dp > ans:
                ans = dp
        return int(ans)
