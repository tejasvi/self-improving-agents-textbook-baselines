class Solution:
    def minimumDifference(self, nums: List[int], k: int) -> int:
        """
        Find a subarray with bitwise OR closest to k.
        
        Key insight: The number of distinct OR values in subarrays ending at 
        position i is at most 30 (number of bits), because once a bit is set,
        it cannot be unset. This makes the solution O(n * log(max_num)).
        
        Algorithm:
        1. For each ending position i, maintain a set of all distinct OR values
           for subarrays ending at i.
        2. When we move to position i+1, we:
           - Include nums[i+1] as a single-element subarray (OR = nums[i+1])
           - OR nums[i+1] with each OR value from position i
        3. Track the minimum absolute difference found.
        """
        min_diff = float('inf')
        
        # current_ors stores all distinct OR values for subarrays ending at current position
        current_ors = set()
        
        for num in nums:
            new_ors = {num}  # Start with the number itself as a single-element subarray
            
            # OR the current number with all previous OR values
            for prev_or in current_ors:
                new_ors.add(prev_or | num)
            
            current_ors = new_ors
            
            # Check the minimum difference for all OR values ending at current position
            for or_value in current_ors:
                diff = abs(k - or_value)
                min_diff = min(min_diff, diff)
                
                # Early termination if we find exact match
                if min_diff == 0:
                    return 0
        
        return min_diff
