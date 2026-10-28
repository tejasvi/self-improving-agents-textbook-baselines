from typing import List


class Solution:
    def maxBalancedSubsequenceSum(self, nums: List[int]) -> int:
        n = len(nums)
        keys = [nums[i] - i for i in range(n)]
        sorted_keys = sorted(set(keys))
        rank = {k: r + 1 for r, k in enumerate(sorted_keys)}
        m = len(sorted_keys)
        tree = [float("-inf")] * (m + 1)

        def update(pos, val):
            while pos <= m:
                if tree[pos] < val:
                    tree[pos] = val
                pos += pos & -pos

        def query(pos):
            best = float("-inf")
            while pos > 0:
                if tree[pos] > best:
                    best = tree[pos]
                pos -= pos & -pos
            return best

        answer = float("-inf")
        for i in range(n):
            r = rank[keys[i]]
            best_prev = query(r)
            dp = nums[i] + (best_prev if best_prev > 0 else 0)
            update(r, dp)
            if dp > answer:
                answer = dp
        return int(answer)
