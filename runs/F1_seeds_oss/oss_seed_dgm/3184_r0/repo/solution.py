from typing import List

class Solution:
    def maxBalancedSubsequenceSum(self, nums: List[int]) -> int:
        """Return maximum sum of a balanced subsequence.
        A subsequence is balanced if for consecutive selected indices i < j we have
        nums[j] - nums[i] >= j - i, which is equivalent to (nums[j] - j) >= (nums[i] - i).
        Hence we need a subsequence where the transformed values a[i] = nums[i] - i are
        non‑decreasing, maximizing the sum of original nums.
        This is a classic maximum‑weight non‑decreasing subsequence problem solved with
        a Fenwick tree (Binary Indexed Tree) after coordinate compression of a[i].
        """
        n = len(nums)
        # Transform values
        a = [nums[i] - i for i in range(n)]
        # Coordinate compression
        sorted_unique = sorted(set(a))
        comp = {v: i + 1 for i, v in enumerate(sorted_unique)}  # 1‑based index for BIT
        size = len(sorted_unique)
        # Fenwick tree for max values
        INF_NEG = -(10**30)
        bit = [INF_NEG] * (size + 1)

        def bit_update(idx: int, value: int) -> None:
            while idx <= size:
                if value > bit[idx]:
                    bit[idx] = value
                idx += idx & -idx

        def bit_query(idx: int) -> int:
            res = INF_NEG
            while idx:
                if bit[idx] > res:
                    res = bit[idx]
                idx -= idx & -idx
            return res

        answer = -10**30
        for i in range(n):
            idx = comp[a[i]]
            best_prev = bit_query(idx)  # maximum dp for a value <= current
            if best_prev == INF_NEG:
                dp = nums[i]
            else:
                dp = best_prev + nums[i]
            # Update BIT with dp at current a value
            bit_update(idx, dp)
            if dp > answer:
                answer = dp
        return answer
