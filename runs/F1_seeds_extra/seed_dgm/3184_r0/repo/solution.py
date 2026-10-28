from typing import List


class Solution:
    def maxBalancedSubsequenceSum(self, nums: List[int]) -> int:
        n = len(nums)
        keys = sorted(set(nums[i] - i for i in range(n)))
        rank = {k: idx + 1 for idx, k in enumerate(keys)}
        m = len(keys)
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

        ans = None
        for i in range(n):
            key = nums[i] - i
            r = rank[key]
            prev = query(r)
            dp = nums[i] + (prev if prev > 0 else 0)
            update(r, dp)
            if ans is None or dp > ans:
                ans = dp
        return ans
