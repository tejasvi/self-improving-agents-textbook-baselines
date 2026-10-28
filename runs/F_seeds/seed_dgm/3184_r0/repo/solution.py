from typing import List


class Solution:
    def maxBalancedSubsequenceSum(self, nums: List[int]) -> int:
        n = len(nums)
        # b[i] = nums[i] - i; a subsequence is balanced iff b is non-decreasing.
        b = [nums[i] - i for i in range(n)]
        vals = sorted(set(b))
        rank = {v: k + 1 for k, v in enumerate(vals)}
        m = len(vals)
        tree = [float('-inf')] * (m + 1)

        def update(pos, val):
            while pos <= m:
                if tree[pos] < val:
                    tree[pos] = val
                pos += pos & -pos

        def query(pos):
            res = float('-inf')
            while pos > 0:
                if tree[pos] > res:
                    res = tree[pos]
                pos -= pos & -pos
            return res

        best = float('-inf')
        for i in range(n):
            r = rank[b[i]]
            prev = query(r)
            cur = nums[i] + (prev if prev > 0 else 0)
            update(r, cur)
            if cur > best:
                best = cur
        return int(best)
