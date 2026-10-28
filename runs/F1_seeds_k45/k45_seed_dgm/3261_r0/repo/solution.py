from typing import List

class Solution:
    def minOrAfterOperations(self, nums: List[int], k: int) -> int:
        """
        Find the minimum possible OR value after at most k operations.
        Each operation combines two adjacent elements using AND.
        
        Strategy:
        - Use a greedy approach with bit positions
        - For each bit from high to low, try to exclude it from the result
        - Check if we can achieve a result without setting that bit
        - If yes, keep it excluded; if no, include it in the result
        """
        
        result = 0
        
        # Try each bit from the highest (29) to the lowest (0)
        for bit in range(29, -1, -1):
            # Try adding this bit to result and check if achievable
            test_result = result | (1 << bit)
            
            # Check if we can achieve a result where OR <= test_result
            if self.canAchieve(nums, k, test_result):
                result = test_result
        
        return result
    
    def canAchieve(self, nums: List[int], k: int, target: int) -> bool:
        """
        Check if we can achieve OR <= target using at most k operations.
        
        Strategy: Greedily combine adjacent elements when their AND produces
        a value that keeps us within the target bit mask.
        """
        # Copy the array for manipulation
        arr = nums[:]
        operations = 0
        
        # Greedy approach: scan through array left to right
        # Combine adjacent elements if it helps us stay within target
        i = 0
        while i < len(arr) - 1 and operations < k:
            # Try combining current and next element
            combined = arr[i] & arr[i + 1]
            
            # Check if this combination helps:
            # We should combine if the AND result has fewer "bad" bits
            # Bad bits are those outside the target mask
            current_bad = (arr[i] | arr[i + 1]) & ~target
            combined_bad = combined & ~target
            
            # If combining reduces bad bits or keeps them same, do it
            if combined_bad <= current_bad:
                arr[i] = combined
                arr.pop(i + 1)
                operations += 1
                # Don't increment i, check again with the new next element
            else:
                i += 1
        
        # Check final OR against target
        final_or = 0
        for num in arr:
            final_or |= num
        
        # Check if final OR is within target (no extra bits set)
        return (final_or & ~target) == 0
