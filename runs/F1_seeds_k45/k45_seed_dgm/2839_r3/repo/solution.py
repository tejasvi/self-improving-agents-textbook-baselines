from typing import List
import bisect

class Solution:
    def maximumSumQueries(self, nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
        """
        Find maximum sum of nums1[j] + nums2[j] for each query [x_i, y_i]
        where nums1[j] >= x_i and nums2[j] >= y_i.
        
        Approach:
        1. Create pairs of (nums1[i], nums2[i]) and sort by nums1 in descending order
        2. Process queries in descending order of x value
        3. For each x threshold, add all pairs with nums1 >= x to candidates
        4. Maintain candidates such that we can quickly find max sum for y threshold
        5. Use a list of (y, max_sum) where y is strictly decreasing and max_sum is non-decreasing
        """
        n = len(nums1)
        
        # Create pairs and sort by nums1 in descending order
        pairs = sorted(zip(nums1, nums2), reverse=True)
        
        # Create list of queries with their original indices
        indexed_queries = [(queries[i][0], queries[i][1], i) for i in range(len(queries))]
        # Sort queries by x value in descending order
        indexed_queries.sort(reverse=True)
        
        result = [-1] * len(queries)
        
        # List to store (y_value, max_sum) pairs
        # Invariant: y_values are in strictly decreasing order
        #            max_sums are in non-decreasing order
        candidates = []
        
        pair_idx = 0
        for x, y, query_idx in indexed_queries:
            # Add all pairs with nums1 >= x
            while pair_idx < n and pairs[pair_idx][0] >= x:
                nums1_val, nums2_val = pairs[pair_idx]
                sum_val = nums1_val + nums2_val
                
                # We need to maintain the invariant:
                # - y_values strictly decreasing
                # - max_sums non-decreasing
                
                # Remove all candidates with y_value <= current nums2_val
                # because current pair has nums2_val which is at least as much,
                # and we want to keep only the best sums for each y range
                while candidates and candidates[-1][0] <= nums2_val:
                    candidates.pop()
                
                # Only add if it improves the maximum sum
                if not candidates or candidates[-1][1] < sum_val:
                    candidates.append((nums2_val, sum_val))
                
                pair_idx += 1
            
            # Find the maximum sum where nums2[j] >= y
            # Since candidates are sorted by y in descending order,
            # we use binary search to find the first candidate with y >= y_threshold
            
            # We're looking for the position where y < y_threshold starts
            y_values = [c[0] for c in candidates]
            
            # bisect_left gives us the leftmost position where y_value >= y
            # But we need y values in ascending order for this
            # So let's use a different approach: iterate from the end
            
            max_sum = -1
            for y_val, sum_val in candidates:
                if y_val >= y:
                    max_sum = sum_val
            
            result[query_idx] = max_sum
        
        return result
