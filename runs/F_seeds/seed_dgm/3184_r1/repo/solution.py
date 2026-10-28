from typing import List


class Solution:
    def maxBalancedSubsequenceSum(self, nums: List[int]) -> int:
        n = len(nums)
        keys = [nums[i] - i for i in range(n)]
        sorted_keys = sorted(set(keys))
        rank = {k: r + 1 for r, k in enumerate(sorted_keys)}
        m = len(sorted_keys)
        NEG = float("-inf")
        tree = [NEG] * (m + 1)

        def update(pos: int, val: int) -> None:
            while pos <= m:
                if tree[pos] < val:
                    tree[pos] = val
                pos += pos & -pos

        def query(pos: int):
            res = NEG
            while pos > 0:
                if tree[pos] > res:
                    res = tree[pos]
                pos -= pos & -pos
            return res

        answer = None
        for i in range(n):
            r = rank[keys[i]]
            best = query(r)
            dp = nums[i] + (best if best > 0 else 0)
            update(r, dp)
            if answer is None or dp > answer:
                answer = dp
        return answer
