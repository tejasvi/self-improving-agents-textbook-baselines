from typing import List
import bisect

class Solution:
    def maximumSumQueries(self, nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
        """
        Find the maximum sum of nums1[j] + nums2[j] for each query where
        nums1[j] >= x_i and nums2[j] >= y_i.
        
        Approach:
        1. Create pairs of (nums1[i], nums2[i]) and sort by nums1 descending
        2. Process queries sorted by y_i descending
        3. Use a sorted list to maintain (nums2_value, max_sum) pairs
        4. For each query, binary search to find max sum where nums2 >= y_i
        """
        n = len(nums1)
        m = len(queries)
        
        # Create list of (nums1[i], nums2[i], sum)
        pairs = [(nums1[i], nums2[i], nums1[i] + nums2[i]) for i in range(n)]
        # Sort by nums1 in descending order
        pairs.sort(reverse=True)
        
        # Create indexed queries: (x, y, original_index)
        indexed_queries = [(queries[i][0], queries[i][1], i) for i in range(m)]
        # Sort queries by y in descending order
        indexed_queries.sort(key=lambda q: -q[1])
        
        result = [-1] * m
        
        # List to store (nums2_value, max_sum_from_this_point_onwards)
        # We maintain this in sorted order by nums2
        sorted_list = []
        
        pair_idx = 0
        
        for x, y, orig_idx in indexed_queries:
            # Add all pairs with nums1 >= x that we haven't processed yet
            # Since pairs are sorted by nums1 descending, we add pairs until nums1 < x
            while pair_idx < n and pairs[pair_idx][0] >= x:
                n1, n2, s = pairs[pair_idx]
                
                # Insert this into sorted_list while maintaining the invariant:
                # For each (nums2_val, max_sum), it represents the max sum achievable
                # with nums2 >= nums2_val
                
                # We only keep entries that could be useful
                # If we have a previous entry with nums2_val' < nums2_val and max_sum' >= max_sum,
                # then this new entry is dominated and we skip it
                
                new_sum = s
                
                # Remove all entries from the end that have max_sum <= new_sum
                # because they are dominated
                while sorted_list and sorted_list[-1][1] <= new_sum:
                    sorted_list.pop()
                
                # Only add if nums2 value is different from last entry
                if not sorted_list or sorted_list[-1][0] != n2:
                    sorted_list.append((n2, new_sum))
                
                pair_idx += 1
            
            # Now find the maximum sum where nums2 >= y
            # sorted_list is sorted by nums2 in ascending order
            # and max_sum is in descending order (by our construction)
            
            if sorted_list:
                # Binary search for the smallest nums2 >= y
                pos = bisect.bisect_left(sorted_list, (y,))
                if pos < len(sorted_list):
                    result[orig_idx] = sorted_list[pos][1]
        
        return result
