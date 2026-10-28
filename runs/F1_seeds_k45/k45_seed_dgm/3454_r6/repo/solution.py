from typing import List

class Solution:
    def minimumOperations(self, nums: List[int], target: List[int]) -> int:
        """
        Calculate the minimum number of operations to make nums equal to target.
        
        Key insight: We can view this problem as tracking "layers" of operations.
        Each operation applies ±1 to a contiguous subarray.
        
        Algorithm:
        1. Calculate the difference array: diff[i] = target[i] - nums[i]
        2. Track the current "level" of operations applied
        3. When moving to the next position, if we need more adjustment,
           we must start new operations
        4. The answer is the sum of all positive level increases
        
        Example 1: nums=[3,5,1,2], target=[4,6,2,4]
        - diff = [1, 1, 1, 2]
        - Start at level 1 (1 operation needed)
        - At index 1: level stays at 1 (already covered)
        - At index 2: level stays at 1 (already covered)
        - At index 3: need level 2 (add 1 operation)
        - Total: 2 operations
        
        Example 2: nums=[1,3,2], target=[2,1,4]
        - diff = [1, -2, 2]
        - Start at level 1 (1 operation needed)
        - At index 1: level goes to -2 (can reduce without extra ops)
        - At index 2: need level 2 (add 4 more operations)
        - Total: 1 + 4 = 5 operations
        """
        n = len(nums)
        
        # Calculate the difference array
        diff = [target[i] - nums[i] for i in range(n)]
        
        # Initialize with the first difference
        operations = abs(diff[0])
        current_level = diff[0]
        
        # Process remaining differences
        for i in range(1, n):
            if diff[i] > current_level:
                # Need to increase the level - requires new operations
                operations += diff[i] - current_level
            # If diff[i] <= current_level, we're already covered
            current_level = diff[i]
        
        return operations
