from typing import List


class Solution:
    def maxBalancedSubsequenceSum(self, nums: List[int]) -> int:
        n = len(nums)
        # b[i] = nums[i] - i; a subsequence is balanced iff b is non-decreasing.
        b = [nums[i] - i for i in range(n)]
        vals = sorted(set(b))
        rank = {v: idx + 1 for idx, v in enumerate(vals)}
        m = len(vals)
        tree = [float("-inf")] * (m + 1)

        def update(pos: int, val: int) -> None:
            while pos <= m:
                if tree[pos] < val:
                    tree[pos] = val
                pos += pos & -pos

        def query(pos: int):
            best = float("-inf")
            while pos > 0:
                if tree[pos] > best:
                    best = tree[pos]
                pos -= pos & -pos
            return best

        ans = float("-inf")
        for i in range(n):
            r = rank[b[i]]
            prev = query(r)  # max dp[j] with b[j] <= b[i], j < i
            cur = nums[i] + (prev if prev > 0 else 0)
            update(r, cur)
            if cur > ans:
                ans = cur
        return int(ans)
