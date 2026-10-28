from typing import List

class Solution:
    def minimumOperations(self, nums: List[int], target: List[int]) -> int:
        """
        The key insight: 
        - Calculate the difference array: diff[i] = target[i] - nums[i]
        - When we perform an operation on a subarray, we change the "flow" through that range
        - The minimum operations is the sum of absolute changes in the flow
        - This equals sum(|diff[i] - diff[i-1]|) for all i, where diff[-1] = 0 and diff[n] = 0
        """
        n = len(nums)
        
        # Calculate the difference array
        diff = [target[i] - nums[i] for i in range(n)]
        
        # Count the minimum operations as the sum of absolute differences between consecutive elements
        operations = 0
        
        # First difference (from 0 to diff[0])
        operations += abs(diff[0])
        
        # Differences between consecutive elements
        for i in range(1, n):
            operations += abs(diff[i] - diff[i-1])
        
        # Final transition (from diff[n-1] to 0)
        operations += abs(diff[n-1])
        
        return operations
