from typing import List

class Solution:
    def maxBalancedSubsequenceSum(self, nums: List[int]) -> int:
        """Return the maximum sum of a balanced subsequence.
        A subsequence is balanced if for consecutive selected indices i < j we have
        nums[j] - nums[i] >= j - i, which is equivalent to (nums[j] - j) >= (nums[i] - i).
        Hence we need the maximum sum subsequence where the transformed values
        a[i] = nums[i] - i are non‑decreasing.
        This is a classic maximum‑sum non‑decreasing subsequence problem and can be
        solved in O(n log n) using a Fenwick tree (Binary Indexed Tree) that stores
        the best sum for each prefix of compressed a[i] values.
        """
        n = len(nums)
        if n == 0:
            return 0

        # Transform values
        transformed = [nums[i] - i for i in range(n)]
        # Coordinate compression
        sorted_unique = sorted(set(transformed))
        comp = {v: i + 1 for i, v in enumerate(sorted_unique)}  # 1‑based index for BIT

        size = len(sorted_unique)
        # Fenwick tree for maximum query
        bit = [float('-inf')] * (size + 1)

        def bit_update(i: int, val: int) -> None:
            while i <= size:
                if val > bit[i]:
                    bit[i] = val
                i += i & -i

        def bit_query(i: int) -> int:
            res = float('-inf')
            while i > 0:
                if bit[i] > res:
                    res = bit[i]
                i -= i & -i
            return res

        best_overall = float('-inf')
        for idx in range(n):
            comp_idx = comp[transformed[idx]]
            # Best sum ending at a previous index with transformed value <= current
            prev_best = bit_query(comp_idx)
            if prev_best < 0:
                prev_best = 0  # start new subsequence
            cur_dp = nums[idx] + prev_best
            # Update structures
            bit_update(comp_idx, cur_dp)
            if cur_dp > best_overall:
                best_overall = cur_dp

        return best_overall
