from typing import List

class Solution:
    def maximumSumQueries(self, nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
        """
        Find maximum sum nums1[j] + nums2[j] for each query where nums1[j] >= x and nums2[j] >= y
        
        Strategy:
        1. Create pairs of (nums1[i], nums2[i]) and sort by nums1 descending
        2. Process queries sorted by x descending
        3. Maintain a monotonic deque of (nums2_val, max_sum) pairs
           - For indices with nums1 >= current x
           - Sorted by nums2 in ascending order
           - With max_sum also in ascending order (monotonic property)
           - This allows efficient query: for y, find the answer among those with nums2 >= y
        """
        n = len(nums1)
        m = len(queries)
        
        # Create list of (nums1[i], nums2[i]) and sort by nums1 descending
        pairs = [(nums1[i], nums2[i]) for i in range(n)]
        pairs.sort(reverse=True)  # Sort by nums1 descending
        
        # Create indexed queries: (x, y, original_index)
        indexed_queries = [(queries[i][0], queries[i][1], i) for i in range(m)]
        # Sort queries by x descending
        indexed_queries.sort(reverse=True)
        
        # Result array
        result = [0] * m
        
        # Monotonic stack: list of (nums2_val, max_sum)
        # Invariant: nums2_val is strictly increasing
        #           max_sum is strictly increasing
        # This ensures: for any y, the answer is the max_sum of the rightmost (nums2_val, max_sum) where nums2_val >= y
        monotonic_stack = []
        
        pair_idx = 0
        
        for x, y, query_idx in indexed_queries:
            # Add all pairs with nums1 >= x to the monotonic stack
            while pair_idx < n and pairs[pair_idx][0] >= x:
                num1_val, num2_val = pairs[pair_idx]
                current_sum = num1_val + num2_val
                
                # Remove elements from stack that have:
                # - nums2 >= current num2_val, OR
                # - smaller sum than current_sum
                while monotonic_stack and (monotonic_stack[-1][0] >= num2_val or monotonic_stack[-1][1] <= current_sum):
                    monotonic_stack.pop()
                
                monotonic_stack.append((num2_val, current_sum))
                
                pair_idx += 1
            
            # Find answer for query (x, y)
            # We need max sum where nums2 >= y among all nums1 >= x
            # All elements in monotonic_stack have nums1 >= x
            # Find the rightmost (nums2_val, max_sum) where nums2_val >= y
            
            result[query_idx] = -1
            for i in range(len(monotonic_stack) - 1, -1, -1):
                if monotonic_stack[i][0] >= y:
                    result[query_idx] = monotonic_stack[i][1]
                    break
        
        return result
