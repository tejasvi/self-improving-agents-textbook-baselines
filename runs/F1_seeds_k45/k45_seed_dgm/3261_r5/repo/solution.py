from typing import List

class Solution:
    def minOrAfterOperations(self, nums: List[int], k: int) -> int:
        """
        Find the minimum possible OR value after at most k AND operations.
        
        Approach:
        - Use a greedy bit-by-bit approach
        - Start with the maximum possible OR (all bits set that appear in nums)
        - Try to turn off bits from MSB to LSB
        - For each bit, check if we can achieve an OR without that bit using at most k operations
        - Use DP to validate if a target OR value is achievable with at most k operations
        """
        
        # Start with all possible bits that could be in the result
        max_bits = max(nums).bit_length() if nums else 1
        result = 0
        
        # Try to build result by considering each bit from MSB to LSB
        for bit in range(max_bits - 1, -1, -1):
            # Try adding this bit to the result (try to NOT have this bit)
            candidate = result | (1 << bit)
            
            # Check if we can achieve OR value of candidate with at most k operations
            if self._canAchieveOr(nums, k, candidate):
                result = candidate
        
        return result
    
    def _canAchieveOr(self, nums: List[int], k: int, target_or: int) -> bool:
        """
        Check if we can achieve an OR value <= target_or with at most k operations.
        We use a greedy approach: combine consecutive elements greedily.
        """
        # This is a greedy check: we try to group elements using AND
        # and see if the combined result has bits only within target_or
        
        n = len(nums)
        operations_used = 0
        i = 0
        
        while i < n:
            # Try to combine as many consecutive elements as possible
            # such that their AND result is compatible with target_or
            combined = nums[i]
            j = i + 1
            
            # Greedily combine while we have operations left and 
            # the AND result is still useful (doesn't add bits outside target_or)
            while j < n and operations_used < k:
                new_combined = combined & nums[j]
                
                # If AND result is compatible with target_or, use the operation
                if (new_combined & target_or) == new_combined:
                    combined = new_combined
                    operations_used += 1
                    j += 1
                else:
                    break
            
            i = j if j > i + 1 else i + 1
        
        # Check final OR
        final_or = 0
        i = 0
        operations_used = 0
        
        while i < n:
            combined = nums[i]
            j = i + 1
            
            while j < n and operations_used < k:
                new_combined = combined & nums[j]
                if (new_combined & target_or) == new_combined:
                    combined = new_combined
                    operations_used += 1
                    j += 1
                else:
                    break
            
            final_or |= combined
            i = j if j > i + 1 else i + 1
        
        return (final_or & target_or) == final_or
