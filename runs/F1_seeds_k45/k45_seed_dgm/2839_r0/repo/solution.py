from typing import List
import bisect

class Solution:
    def maximumSumQueries(self, nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums1)
        m = len(queries)
        
        # Create pairs of (nums1[i], nums2[i])
        pairs = [(nums1[i], nums2[i]) for i in range(n)]
        
        # Sort pairs by nums1 in descending order
        pairs.sort(reverse=True)
        
        # Create queries with their original indices
        indexed_queries = [(queries[i][0], queries[i][1], i) for i in range(m)]
        
        # Sort queries by x (nums1 threshold) in descending order
        indexed_queries.sort(reverse=True)
        
        # Result array
        result = [0] * m
        
        # Maintain a list of (nums2_value, max_sum) in sorted order
        # This represents the Pareto frontier - for each nums2 value,
        # we track the maximum sum seen so far
        monotonic_stack = []  # List of (nums2, sum) sorted by nums2
        
        pair_idx = 0
        
        for x, y, original_idx in indexed_queries:
            # Add all pairs with nums1 >= x to our monotonic stack
            while pair_idx < n and pairs[pair_idx][0] >= x:
                num1, num2 = pairs[pair_idx]
                current_sum = num1 + num2
                
                # Remove dominated entries from the stack
                # An entry (n2, s) is dominated if there's another entry (n2', s') 
                # where n2' >= n2 and s' >= s
                while monotonic_stack and monotonic_stack[-1][1] <= current_sum:
                    monotonic_stack.pop()
                
                # Only add if it's not dominated by the last entry
                if not monotonic_stack or monotonic_stack[-1][0] < num2:
                    monotonic_stack.append((num2, current_sum))
                
                pair_idx += 1
            
            # Now find the maximum sum where nums2 >= y
            if not monotonic_stack:
                result[original_idx] = -1
            else:
                # Binary search for the first nums2 >= y
                # We need to find the rightmost position where nums2 < y
                pos = bisect.bisect_left(monotonic_stack, (y,))
                
                if pos < len(monotonic_stack):
                    # There's an entry with nums2 >= y
                    # Find the maximum sum from pos onwards
                    max_sum = -1
                    for i in range(pos, len(monotonic_stack)):
                        max_sum = max(max_sum, monotonic_stack[i][1])
                    result[original_idx] = max_sum
                else:
                    result[original_idx] = -1
        
        return result
