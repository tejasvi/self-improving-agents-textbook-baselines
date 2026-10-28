from typing import List

class Solution:
    def minimumOperations(self, nums: List[int], target: List[int]) -> int:
        """
        Compute the minimum number of operations to make nums equal to target.
        
        Key insight: Create a difference array diff[i] = target[i] - nums[i].
        Think of this as a profile where we need to build heights using operations.
        Each operation incrementally or decrementally applies to a contiguous subarray.
        
        The minimum operations is the sum of all positive changes in the profile:
        - When we go "up" in the profile, we need to open new operations
        - When we go "down", operations end (no new operations needed)
        - The total is the sum of all upward movements
        
        This is equivalent to: sum(max(0, diff[i] - diff[i-1])) for all i
        starting from a virtual diff[-1] = 0.
        """
        n = len(nums)
        diff = [target[i] - nums[i] for i in range(n)]
        
        operations = 0
        prev_diff = 0
        
        for current_diff in diff:
            # Count only positive changes (going up in the profile)
            if current_diff > prev_diff:
                operations += current_diff - prev_diff
            prev_diff = current_diff
        
        return operations
