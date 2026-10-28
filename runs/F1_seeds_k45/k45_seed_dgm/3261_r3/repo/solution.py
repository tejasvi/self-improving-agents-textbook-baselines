from typing import List

class Solution:
    def minOrAfterOperations(self, nums: List[int], k: int) -> int:
        """
        Minimize the OR of remaining elements using at most k AND operations.
        
        Strategy:
        - Use greedy bit-by-bit approach
        - Try to build the minimum result by clearing bits from MSB to LSB
        - Use a sliding window to check if a candidate result is achievable
        """
        
        # Start with OR of all elements (no operations)
        result = 0
        for num in nums:
            result |= num
        
        # Try to turn off each bit from most significant to least significant
        # Bits in result that are 0 will stay 0
        for bit in range(29, -1, -1):
            # Try to turn off this bit
            candidate = result - (1 << bit)  # Remove this bit from result
            
            # Check if we can achieve this result with at most k operations
            if self._canAchieve(nums, k, candidate):
                result = candidate
        
        return result
    
    def _canAchieve(self, nums: List[int], k: int, target: int) -> bool:
        """
        Check if we can achieve a target OR value with at most k operations.
        We use a sliding window approach to see if we can reduce elements 
        such that their OR equals target.
        """
        # We need to check if we can partition/merge the array
        # such that the OR of the remaining elements equals target
        
        # Use a greedy sliding window approach
        # Try to use operations to merge consecutive elements
        # whenever merging helps us
        
        operations_used = 0
        i = 0
        
        while i < len(nums):
            # Start a new window at position i
            current_and = nums[i]
            j = i + 1
            
            # Keep merging while AND of elements in window doesn't have bits outside target
            while j < len(nums) and operations_used < k:
                new_and = current_and & nums[j]
                
                # If new_and has all bits within target, we can consider merging
                if (new_and & ~target) == 0:
                    current_and = new_and
                    j += 1
                    operations_used += 1
                else:
                    break
            
            # If current_and has bits outside target, we can't achieve target
            if (current_and & ~target) != 0:
                return False
            
            i = j
        
        return True
