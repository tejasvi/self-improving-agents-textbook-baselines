from typing import List

class Solution:
    def minOrAfterOperations(self, nums: List[int], k: int) -> int:
        """
        Minimize the bitwise OR of remaining elements after at most k AND operations.
        
        Strategy:
        - Use a greedy approach with bit manipulation
        - Process bits from high to low (from bit 29 down to 0)
        - For each bit, try to make it 0 in the final result
        - To achieve this, partition the array into groups where each group's AND has that bit as 0
        - If we can partition with at most k merge operations, we keep trying to zero out that bit
        - Otherwise, include that bit in the answer and move to the next bit
        """
        if not nums:
            return 0
        
        result = 0
        
        # Process each bit from high to low (bit 29 down to 0)
        for bit in range(29, -1, -1):
            # Try to set this bit to 0 in the result
            # We use a greedy approach: try to partition the array such that
            # each partition's AND has this bit as 0
            
            # Create a mask for bits we've already decided to keep (result so far)
            temp_mask = result | (1 << bit)
            
            # Check if we can partition the array with at most k operations
            # such that the AND of each group AND-ed together gives temp_mask bits as 0
            if can_achieve_mask(nums, k, temp_mask):
                # We can make this bit 0, so don't include it in result
                continue
            else:
                # We can't make this bit 0, so include it in result
                result |= (1 << bit)
        
        return result


def can_achieve_mask(nums: List[int], k: int, target_mask: int) -> bool:
    """
    Check if we can partition nums into groups using at most k AND operations
    such that the final OR result has only the bits in target_mask.
    
    In other words, check if any bit that's NOT in target_mask is 0 
    in the OR of all groups.
    
    This is equivalent to: can we partition the array such that
    for each bit NOT in target_mask, at least one element in each group has that bit as 0.
    
    Simplified: can we partition with at most k merges such that 
    the AND of all elements AND-ed together produces a result with no extra bits beyond target_mask?
    
    Actually, the key insight: we want to know if we can reduce the OR to only have bits in target_mask.
    This means: can we partition such that each group has AND result that only contributes bits in target_mask?
    """
    
    # We use a greedy approach: go through elements from left to right
    # and try to form groups where the AND of each group is a subset of target_mask
    
    current_and = nums[0]
    operations_used = 0
    
    for i in range(1, len(nums)):
        next_and = current_and & nums[i]
        
        # Check if the next AND would produce bits outside target_mask
        if (next_and & target_mask) != next_and:
            # next_and has bits not in target_mask, can't merge
            # Start a new group
            current_and = nums[i]
            operations_used += 1
        else:
            # We can merge, or we can start a new group
            # Greedy: always merge if possible to preserve operations
            current_and = next_and
            operations_used += 1
    
    return operations_used <= k
