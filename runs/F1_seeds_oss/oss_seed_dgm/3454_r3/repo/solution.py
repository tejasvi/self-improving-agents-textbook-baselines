from typing import List

class Solution:
    def minimumOperations(self, nums: List[int], target: List[int]) -> int:
        """Return the minimum number of subarray increment/decrement operations
        required to transform `nums` into `target`.

        The problem can be reduced to the difference array `diff[i] = target[i] - nums[i]`.
        An operation adds +1 or -1 to a contiguous subarray, which corresponds to
        starting (or ending) a “level” of increments or decrements.
        By handling positive and negative parts independently we obtain a greedy
        linear solution:

        * Let `pos[i] = max(diff[i], 0)` and `neg[i] = max(-diff[i], 0)`.
        * While scanning left‑to‑right, whenever `pos[i]` is larger than the previous
          positive level we need `pos[i] - prev_pos` new increment operations that start
          at index `i`.
        * Similarly, when `neg[i]` exceeds the previous negative level we need
          `neg[i] - prev_neg` new decrement operations.
        * The sum of all these increases gives the minimal number of operations.
        """
        total_ops = 0
        prev_pos = 0  # previous positive level
        prev_neg = 0  # previous negative level
        for n, t in zip(nums, target):
            diff = t - n
            cur_pos = diff if diff > 0 else 0
            cur_neg = -diff if diff < 0 else 0
            if cur_pos > prev_pos:
                total_ops += cur_pos - prev_pos
            if cur_neg > prev_neg:
                total_ops += cur_neg - prev_neg
            prev_pos = cur_pos
            prev_neg = cur_neg
        return total_ops
