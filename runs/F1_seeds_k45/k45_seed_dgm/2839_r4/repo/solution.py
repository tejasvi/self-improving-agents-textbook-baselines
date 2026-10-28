from typing import List
from bisect import bisect_left

class Solution:
    def maximumSumQueries(self, nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
        """
        Find maximum sum nums1[j] + nums2[j] for each query (x, y) where nums1[j] >= x and nums2[j] >= y.
        
        Strategy:
        1. Create pairs of (nums1[i], nums2[i]) and sort by nums1 in descending order
        2. Process queries from highest to lowest x value to build a data structure
        3. For each x threshold, maintain a list of (nums2[j], sum[j]) in sorted order
        4. Binary search for the minimum nums2[j] >= y and get the maximum sum
        """
        n = len(nums1)
        m = len(queries)
        
        # Create list of (nums1, nums2, original_sum)
        pairs = []
        for i in range(n):
            pairs.append((nums1[i], nums2[i], nums1[i] + nums2[i]))
        
        # Sort by nums1 in descending order
        pairs.sort(reverse=True)
        
        # Create query indices with their x and y values
        query_indices = list(range(m))
        query_indices.sort(key=lambda i: queries[i][0], reverse=True)
        
        # Result array
        answer = [0] * m
        
        # List to maintain (nums2, max_sum) pairs in sorted order by nums2
        # This represents the best sums we can achieve for different nums2 values
        sorted_pairs = []
        
        pair_idx = 0
        
        for qi in query_indices:
            x, y = queries[qi]
            
            # Add all pairs with nums1 >= x to our sorted_pairs
            while pair_idx < n and pairs[pair_idx][0] >= x:
                nums1_val, nums2_val, sum_val = pairs[pair_idx]
                
                # Add this pair to sorted_pairs
                # But we need to maintain only the useful pairs
                # A pair (nums2_a, sum_a) is useful only if:
                # - there's no other pair (nums2_b, sum_b) where nums2_b >= nums2_a and sum_b > sum_a
                
                # Remove pairs that are dominated by this new pair
                while sorted_pairs and sorted_pairs[-1][0] <= nums2_val and sorted_pairs[-1][1] <= sum_val:
                    sorted_pairs.pop()
                
                if not sorted_pairs or sorted_pairs[-1][1] < sum_val:
                    sorted_pairs.append((nums2_val, sum_val))
                
                pair_idx += 1
            
            # Now find the answer for query (x, y)
            # We need nums2 >= y, so binary search in sorted_pairs
            if sorted_pairs:
                # Binary search for the position where nums2 >= y
                pos = bisect_left(sorted_pairs, (y,))
                
                if pos < len(sorted_pairs):
                    # Find the maximum sum among all pairs with nums2 >= y
                    max_sum = max(pair[1] for pair in sorted_pairs[pos:])
                    answer[qi] = max_sum
                else:
                    answer[qi] = -1
            else:
                answer[qi] = -1
        
        return answer
