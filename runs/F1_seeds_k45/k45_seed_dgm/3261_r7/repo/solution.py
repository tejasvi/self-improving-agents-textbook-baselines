class Solution:
    def minOrAfterOperations(self, nums: List[int], k: int) -> int:
        """
        Minimize the bitwise OR after at most k operations of ANDing adjacent elements.
        
        Strategy:
        - Build the answer bit by bit from high to low
        - For each bit position, check if we can exclude it from the final result
        - To exclude a bit, every final number must have that bit as 0
        - We count: given k operations, can we partition the array so each partition has bit 0?
        """
        result = 0
        
        # Try each bit from highest (29) to lowest (0)
        for bit in range(29, -1, -1):
            # Try to see if we can keep this bit out of the final result
            if canExcludeBit(nums, k, bit):
                # If we can exclude this bit, don't add it to result
                pass
            else:
                # If we can't exclude this bit, it must be in the result
                result |= (1 << bit)
        
        return result


def canExcludeBit(nums, k, bit):
    """
    Check if we can exclude 'bit' position from the final OR
    by using at most k operations.
    
    Strategy: Greedily form segments where each segment's AND has the target bit as 0.
    We AND consecutive numbers starting from position i until the AND becomes 0 at target bit.
    If segment ends at position j, we have j - i + 1 numbers merged into 1, costing j - i operations.
    Total cost = n - (number of segments).
    """
    n = len(nums)
    segments = 0
    i = 0
    
    while i < n:
        current_and = -1  # All bits set
        j = i
        segment_found = False
        
        # AND consecutive numbers starting from position i
        while j < n:
            current_and &= nums[j]
            
            # Check if the target bit is now 0
            if not (current_and & (1 << bit)):
                # Found a segment from i to j
                segments += 1
                i = j + 1
                segment_found = True
                break
            
            j += 1
        
        if not segment_found:
            # Couldn't form a segment with bit 0 from position i to end
            # This means we can't exclude this bit
            return False
    
    # Total cost = n - segments (number of operations needed)
    operations = n - segments
    return operations <= k
