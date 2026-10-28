from typing import List


class Solution:
    def minimumOperations(self, nums: List[int], target: List[int]) -> int:
        """Return the minimum number of subarray +-1 operations to transform nums into target.

        The problem reduces to transforming the difference array `a[i] = target[i] - nums[i]`
        to all zeros using operations that add +1 or -1 to a contiguous subarray. In terms of the
        first‑difference array `b`, where `b[0] = a[0]` and `b[i] = a[i] - a[i-1]` for i > 0,
        each operation adds +1 to `b[l]` and -1 to `b[r+1]` (or the opposite for a decrement).
        Hence an operation simply moves one unit of value from one position of `b` to another.
        The minimal number of such unit moves required to zero out `b` is the total amount that
        must be moved, i.e. the sum of the positive entries of `b` (which equals half of the sum
        of absolute values because the total sum of `b` is zero).

        We can compute this in O(n) time without constructing the entire `b` array: keep track of
        the previous cumulative difference `prev`. For each index we compute `cur = diff - prev`
        where `diff = target[i] - nums[i]`. The positive part of `cur` contributes to the answer.
        After processing all elements we also need to account for the final transition back to
        zero, i.e. `-prev`.
        """
        ans = 0
        prev = 0
        for n, t in zip(nums, target):
            diff = t - n
            cur = diff - prev
            if cur > 0:
                ans += cur
            prev = diff
        # final step to bring the last prefix back to zero
        if prev < 0:
            ans += -prev
        return ans
