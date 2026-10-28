from typing import List

class Solution:
    def minOrAfterOperations(self, nums: List[int], k: int) -> int:
        """
        Minimize the bitwise OR of remaining elements after at most k operations.
        
        Key insight: Use a greedy approach with a sliding window/mask-building strategy.
        - Try to clear bits from high to low
        - For each bit, check if we can make it 0 by combining adjacent elements
        - Use dynamic programming with greedy bit clearing
        
        The idea is:
        1. Start with a result mask of all 1s
        2. For each bit from 29 down to 0, check if we can achieve a result without that bit
        3. For each potential result mask, check if it's achievable with at most k operations
        """
        n = len(nums)
        
        # Start with maximum possible OR (all bits set)
        result = 0
        for num in nums:
            result |= num
        
        # Try to clear each bit from high to low
        for bit in range(29, -1, -1):
            # Try to clear this bit from the result
            candidate = result ^ (1 << bit)  # Clear the bit
            
            # Check if we can achieve this candidate result with at most k operations
            if self.canAchieve(nums, k, candidate):
                result = candidate
        
        return result
    
    def canAchieve(self, nums: List[int], k: int, target: int) -> bool:
        """
        Check if we can achieve a result with OR <= target using at most k operations.
        
        Greedy approach:
        - Use a sliding window where we combine adjacent elements
        - When current AND with remaining elements would exceed target, combine them
        - Count operations and check if <= k
        """
        n = len(nums)
        operations = 0
        i = 0
        
        while i < n:
            # Start accumulating AND from position i
            current_and = nums[i]
            j = i + 1
            
            # Extend the window as long as (current_and & nums[j]) doesn't have bits outside target
            while j < n and (current_and & nums[j]) & ~target == 0:
                # We can potentially combine nums[i:j+1]
                # But we need to check if combining them would help
                current_and &= nums[j]
                j += 1
            
            # If we couldn't extend beyond i+1, we need to combine
            if j == i + 1:
                j = i + 2  # Combine at least i and i+1
            
            # j now points to the position after the last element to combine
            # We perform (j - i - 1) operations to combine elements from i to j-1
            ops_needed = j - i - 1
            operations += ops_needed
            
            if operations > k:
                return False
            
            i = j
        
        return True
