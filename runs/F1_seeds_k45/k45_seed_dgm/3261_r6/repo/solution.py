from typing import List

class Solution:
    def minOrAfterOperations(self, nums: List[int], k: int) -> int:
        """
        Strategy:
        - Use a greedy approach with bit manipulation
        - For each bit position (from MSB to LSB), try to make it 0 in the result OR
        - Use a sliding window approach: for each position, try to AND consecutive elements
          using at most k operations, and check if we can achieve the target without setting
          that particular bit
        - Build the result bit by bit
        """
        
        result = 0
        
        # Try each bit from 29 down to 0 (since nums[i] < 2^30)
        for bit in range(29, -1, -1):
            # Try to avoid setting this bit in the result
            operations_left = k
            i = 0
            can_avoid_bit = True
            
            while i < len(nums):
                current_and = nums[i]
                j = i + 1
                
                # Try to AND consecutive elements to eliminate this bit
                while j < len(nums) and operations_left > 0 and (current_and & (1 << bit)):
                    current_and &= nums[j]
                    operations_left -= 1
                    j += 1
                
                # Check if this element still has the bit set
                if current_and & (1 << bit):
                    can_avoid_bit = False
                    break
                
                i = j
            
            # If we can't avoid setting this bit, we must set it
            if not can_avoid_bit:
                result |= (1 << bit)
        
        return result
