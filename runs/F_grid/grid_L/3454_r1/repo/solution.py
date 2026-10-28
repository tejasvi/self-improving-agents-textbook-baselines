from typing import List


class Solution:
    def minimumOperations(self, nums: List[int], target: List[int]) -> int:
        # Let d = target - nums, padded with 0 at both ends.
        # An operation on [l, r] adds +v at index l and -v at index r+1 of the
        # difference array of d (v = +1 or -1). The minimum number of operations
        # is the sum of positive jumps of the padded array d.
        prev = 0
        res = 0
        for a, b in zip(nums, target):
            cur = b - a
            if cur > prev:
                res += cur - prev
            prev = cur
        # Transition from the last element back to the padded 0.
        if prev < 0:
            res += -prev
        return res
