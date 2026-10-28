from typing import List

class Solution:
    def maxValue(self, nums: List[int], k: int) -> int:
        """
        Find the maximum value of a subsequence of size 2*k where:
        value = (OR of first k elements) XOR (OR of second k elements)
        
        Strategy:
        We need to partition n elements into 3 groups:
        - First k elements (for first OR)
        - Next k elements (for second OR)  
        - Remaining n - 2k elements (unused)
        
        Since OR values have limited distinct values (at most 128 for values < 128),
        we can use DP to track reachable OR values.
        
        dp[i][j] = set of all possible OR values using exactly j elements from nums[0:i]
        
        We'll iterate through the array and for each position, track all possible 
        OR values we can achieve.
        """
        n = len(nums)
        
        # dp[i][j] = set of possible OR values using exactly j elements from nums[0:i]
        dp = [[set() for _ in range(k + 1)] for _ in range(n + 1)]
        dp[0][0].add(0)
        
        # Build DP table
        for i in range(n):
            for j in range(k + 1):
                # Case 1: Don't take nums[i]
                dp[i + 1][j].update(dp[i][j])
                
                # Case 2: Take nums[i]
                if j > 0:
                    for or_val in dp[i][j - 1]:
                        dp[i + 1][j].add(or_val | nums[i])
        
        # All possible OR values using exactly k elements from the entire array
        first_half_ors = dp[n][k]
        
        max_result = 0
        
        # Now, for each possible first half OR value, we need to find 
        # the best second half OR value from the remaining elements
        # But we don't know which specific k elements formed that OR value
        
        # Key insight: We need to use DP differently
        # We iterate through the array and at each step, track:
        # "What OR values can I get for first half after seeing first i elements?"
        # "What OR values can I get for second half after seeing remaining elements?"
        
        # Better approach: for each split in selecting first k elements and second k elements
        # we can use DP on subsets
        
        # Let's use a smarter method:
        # Process array left to right, maintaining DP states for both halves
        
        # dp_left[i][j] = set of OR values using j elements from nums[0:i]
        # For each state, we want to extend it with second half selections
        
        # Actually, let me think differently:
        # At position i, we have selected:
        # - left_count elements for first half
        # - right_count elements for second half  
        # - remaining elements ignored
        # Total selected: left_count + right_count <= i
        
        # dp[i][left_count][right_count] = set of (first_or, second_or) pairs
        # But this might be too memory intensive
        
        # Let me use a different strategy that's cleaner:
        # For each possible first half OR value, compute the second half DP
        # starting fresh from the entire array (but we don't use the same element twice)
        
        # This is tricky. Let me use a cleaner DP formulation:
        # dp[i][j][k] where:
        # i = position in array
        # j = elements selected for first half so far
        # k = elements selected for second half so far
        # value = set of (first_or, second_or) pairs possible
        
        # But this is O(n * k * k * max_states) which might be large
        
        # Actually, simpler approach that should work:
        # Since we want to maximize first_or XOR second_or,
        # and OR values are bounded to 128 values,
        # we can just compute all possible first_or values and all possible second_or values
        # independently, then try all combinations.
        
        # The issue is ensuring we don't use the same element twice.
        # But here's the key: we can use a DP that respects element usage.
        
        # Let me implement a DP with three dimensions:
        # State: (position, count_in_first_half, count_in_second_half)
        # Value: set of (or_value_first, or_value_second) tuples
        
        from collections import defaultdict
        
        # dp[j][k] = set of (first_or, second_or) pairs where 
        # j = count of elements in first half
        # k = count of elements in second half
        
        dp_state = [[set() for _ in range(k + 1)] for _ in range(k + 1)]
        dp_state[0][0].add((0, 0))
        
        for num in nums:
            # Process in reverse to avoid using same element twice
            new_dp = [[s.copy() for s in row] for row in dp_state]
            
            for j in range(k):
                for m in range(k):
                    for first_or, second_or in dp_state[j][m]:
                        # Add to first half
                        new_dp[j + 1][m].add((first_or | num, second_or))
                        # Add to second half  
                        new_dp[j][m + 1].add((first_or, second_or | num))
            
            dp_state = new_dp
        
        # Extract result
        for first_or, second_or in dp_state[k][k]:
            result = first_or ^ second_or
            max_result = max(max_result, result)
        
        return max_result
