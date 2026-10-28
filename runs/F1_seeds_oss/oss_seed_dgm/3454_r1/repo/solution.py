from typing import List

class Solution:
    def minimumOperations(self, nums: List[int], target: List[int]) -> int:
        """Return the minimum number of subarray +/-1 operations to turn nums into target.
        
        Let diff[i] = target[i] - nums[i]. We start from an all‑zero array and want to obtain
        `diff` using operations that add +1 or -1 to any contiguous subarray.  Each operation
        creates a +1 step at the left boundary of the chosen subarray and a -1 step just after
        the right boundary (or only one step if the subarray touches an array end).  Consequently
        the sequence of differences between consecutive elements of `diff` (with a virtual 0
        before the first element and after the last) must be covered by such steps.
        
        The total variation V = |diff[0]| + Σ_{i=1}^{n-1} |diff[i] - diff[i-1]| + |diff[n-1]|
        counts each operation twice (once for its +1 step and once for its -1 step).  Therefore
        the minimal number of operations is V // 2.
        """
        n = len(nums)
        total_variation = 0
        prev = 0  # virtual diff[-1]
        for i in range(n):
            cur = target[i] - nums[i]
            total_variation += abs(cur - prev)
            prev = cur
        total_variation += abs(prev)  # account for returning to 0 after last element
        return total_variation // 2
