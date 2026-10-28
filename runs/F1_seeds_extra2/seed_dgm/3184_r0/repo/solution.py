from typing import List


class Solution:
    def maxBalancedSubsequenceSum(self, nums: List[int]) -> int:
        n = len(nums)
        keys = sorted(set(nums[i] - i for i in range(n)))
        rank = {k: idx + 1 for idx, k in enumerate(keys)}
        m = len(keys)
        tree = [float("-inf")] * (m + 1)

        def update(pos, val):
            while pos <= m:
                if tree[pos] < val:
                    tree[pos] = val
                pos += pos & -pos

        def query(pos):
            res = float("-inf")
            while pos > 0:
                if tree[pos] > res:
                    res = tree[pos]
                pos -= pos & -pos
            return res

        best = float("-inf")
        for i in range(n):
            r = rank[nums[i] - i]
            prev = query(r)
            dp = nums[i] + (prev if prev > 0 else 0)
            update(r, dp)
            if dp > best:
                best = dp
        return int(best)
