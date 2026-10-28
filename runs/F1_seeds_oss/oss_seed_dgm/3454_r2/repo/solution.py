from typing import List

class Solution:
    def minimumOperations(self, nums: List[int], target: List[int]) -> int:
        """Return the minimum number of subarray +/-1 operations to turn nums into target.

        The problem can be transformed by considering the difference array D where D[i] = target[i] - nums[i].
        An operation adds +1 or -1 to a contiguous subarray of nums, which corresponds to adding the same value to a contiguous
        subarray of D, i.e., decreasing D towards zero.  Using the classic "difference array" trick, a +1 operation on subarray
        [l, r] adds +1 to diff[l] and -1 to diff[r+1] where diff is the first‑order difference of D (with an implicit diff entry
        after the last element equal to -D[-1]).  To make all entries of D zero we must cancel all positive and negative entries
        of this extended diff array.  Each operation introduces exactly one +1 in diff (at the start of the interval), so the
        minimal number of operations equals the total magnitude of positive entries in the extended diff array.

        Concretely, let D[i] = target[i] - nums[i].  Define diff[0] = D[0] and for i>0 diff[i] = D[i] - D[i-1]; also diff[n] = -D[n-1].
        The answer is sum(max(0, diff[i])) for i = 0..n.
        This can be computed in O(n) time and O(1) extra space.
        """
        n = len(nums)
        if n == 0:
            return 0
        # First difference
        prev = target[0] - nums[0]
        ans = prev if prev > 0 else 0
        for i in range(1, n):
            cur = target[i] - nums[i]
            diff = cur - prev
            if diff > 0:
                ans += diff
            prev = cur
        # handle the trailing diff that brings the cumulative sum back to zero
        if prev < 0:
            ans += -prev
        return ans
