class Solution:
    def minimumDifference(self, nums: List[int], k: int) -> int:
        """
        Find a subarray with bitwise OR closest to k.
        
        Algorithm:
        - For each position j, maintain a set of all unique OR values 
          for subarrays ending at j
        - The number of unique OR values is bounded by ~30 (number of bits)
        - Time complexity: O(n * 30) = O(n)
        - Space complexity: O(30) = O(1)
        """
        min_diff = float('inf')
        # current_ors: set of all possible OR values for subarrays ending at current position
        current_ors = set()
        
        for num in nums:
            # Create new set for subarrays ending at this position
            new_ors = {num}  # Start with the number itself (subarray of length 1)
            
            # OR the current number with all previous OR values
            for prev_or in current_ors:
                new_ors.add(prev_or | num)
            
            current_ors = new_ors
            
            # Check the minimum difference for all OR values ending at this position
            for or_val in current_ors:
                min_diff = min(min_diff, abs(k - or_val))
        
        return min_diff
