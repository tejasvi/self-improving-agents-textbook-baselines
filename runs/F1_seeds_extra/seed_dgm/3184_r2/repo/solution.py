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
            res = NEG
            while pos > 0:
                if tree[pos] > res:
                    res = tree[pos]
                pos -= pos & -pos
            return res

        ans = None
        for i in range(n):
            key = nums[i] - i
            r = rank[key]
            best = query(r)  # max dp[j] with nums[j]-j <= nums[i]-i
            cur = nums[i] + (best if best > 0 else 0)
            update(r, cur)
            if ans is None or cur > ans:
                ans = cur
        return ans
