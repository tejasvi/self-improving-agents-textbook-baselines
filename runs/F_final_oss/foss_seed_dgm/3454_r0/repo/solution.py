from typing import List

class Solution:
    def minimumOperations(self, nums: List[int], target: List[int]) -> int:
        """Return the minimum number of subarray increment/decrement operations
        required to transform `nums` into `target`.

        The operation can add +1 or -1 to every element of an arbitrary contiguous
        subarray.  This problem can be solved by looking at the difference array
        `diff[i] = target[i] - nums[i]`.  Any operation corresponds to adding +1 or
        -1 to a prefix of `diff` (when expressed via a difference of a difference
        array).  The number of operations needed for positive increments and
        negative decrements can be counted separately using a classic "mountain"
        counting technique.

        For the positive part we consider `pos[i] = max(diff[i], 0)`.  Starting
        from zero, each time `pos[i]` is larger than `pos[i-1]` we need to start
        `pos[i] - pos[i-1]` new increment operations that will continue to the
        right.  The total number of increment operations is therefore
        `pos[0] + sum(max(pos[i] - pos[i-1], 0) for i in 1..n-1)`.  The same logic
        applies to the negative part, using `neg[i] = max(-diff[i], 0)`.

        The answer is the sum of the two counts.
        """
        n = len(nums)
        pos_prev = 0  # previous positive requirement
        neg_prev = 0  # previous negative requirement
        ops = 0
        for i in range(n):
            diff = target[i] - nums[i]
            pos = diff if diff > 0 else 0
            neg = -diff if diff < 0 else 0
            if pos > pos_prev:
                ops += pos - pos_prev
            if neg > neg_prev:
                ops += neg - neg_prev
            pos_prev = pos
            neg_prev = neg
        return ops
