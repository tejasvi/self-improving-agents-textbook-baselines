from typing import List


class Solution:
    def maxBalancedSubsequenceSum(self, nums: List[int]) -> int:
        n = len(nums)
        keys = sorted(set(nums[i] - i for i in range(n)))
        rank = {k: r + 1 for r, k in enumerate(keys)}
        m = len(keys)
        tree = [float("-inf")] * (m + 1)

        def update(pos, val):
            while pos <= m:
                if tree[pos] < val:
                    tree[pos] = val
                pos += pos & -pos

        def query(pos):
            best = 0
            while pos > 0:
                if tree[pos] > best:
                    best = tree[pos]
                pos -= pos & -pos
            return best

        ans = float("-inf")
        for i in range(n):
            r = rank[nums[i] - i]
            dp = nums[i] + query(r)
            update(r, dp)
            if dp > ans:
                ans = dp
        return int(ans)
