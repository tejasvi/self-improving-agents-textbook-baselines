from typing import List

class Solution:
    def maxBalancedSubsequenceSum(self, nums: List[int]) -> int:
        # Transform the condition: nums[i] - nums[j] >= i - j  <=>  (nums[i] - i) >= (nums[j] - j)
        # Hence we need a subsequence where a_i = nums[i] - i is non‑decreasing.
        # We want the maximum sum of original nums over such a subsequence.
        # This is a weighted longest non‑decreasing subsequence problem.
        # Use a Fenwick (Binary Indexed) tree storing the maximum dp value for each prefix of compressed a_i.

        n = len(nums)
        a = [nums[i] - i for i in range(n)]
        # Coordinate compression of a values
        uniq = sorted(set(a))
        comp = {v: i + 1 for i, v in enumerate(uniq)}  # 1‑based index for BIT
        size = len(uniq)

        # Fenwick tree for max query on prefix
        INF_NEG = -10**18
        bit = [INF_NEG] * (size + 1)

        def bit_update(idx: int, value: int) -> None:
            while idx <= size:
                if value > bit[idx]:
                    bit[idx] = value
                idx += idx & -idx

        def bit_query(idx: int) -> int:
            # maximum on prefix [1..idx]
            res = INF_NEG
            while idx > 0:
                if bit[idx] > res:
                    res = bit[idx]
                idx -= idx & -idx
            return res

        answer = -10**18
        for i, val in enumerate(nums):
            idx = comp[a[i]]
            best = bit_query(idx)
            # If no previous element satisfies the condition, best will be INF_NEG.
            # In that case we start a new subsequence with only current element.
            if best < 0:
                best = 0
            dp = val + best
            # Update structures
            bit_update(idx, dp)
            if dp > answer:
                answer = dp
        return answer
