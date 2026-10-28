from typing import List

class Solution:
    def maximumSumQueries(self, nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
        """
        For each query (x, y), find max(nums1[j] + nums2[j]) where nums1[j] >= x and nums2[j] >= y.
        
        Approach:
        1. Create pairs of (num1, num2, sum) and sort by num1 descending
        2. Sort queries with their original indices
        3. Process queries in order of decreasing x values
        4. Maintain a list of (num2, max_sum) values seen so far
        5. For each query, do a binary search on num2 values to find max sum
        """
        n = len(nums1)
        
        # Create list of (nums1[i], nums2[i], sum)
        pairs = [(nums1[i], nums2[i], nums1[i] + nums2[i]) for i in range(n)]
        
        # Sort pairs by nums1 in descending order
        pairs.sort(reverse=True)
        
        # Create list of (query, original_index)
        query_list = [(queries[i][0], queries[i][1], i) for i in range(len(queries))]
        
        # Sort queries by x (nums1 constraint) in descending order
        query_list.sort(reverse=True)
        
        # Result array
        result = [0] * len(queries)
        
        # List to maintain (y_value, max_sum) pairs
        # This stores the best maximum sum for each y threshold
        monotonic_pairs = []
        
        pair_idx = 0
        
        for x, y, query_idx in query_list:
            # Add all pairs where nums1 >= x to monotonic_pairs
            while pair_idx < n and pairs[pair_idx][0] >= x:
                num1, num2, total = pairs[pair_idx]
                
                # Add this (num2, total) to monotonic_pairs
                # Remove any pairs that are dominated
                while monotonic_pairs and monotonic_pairs[-1][1] <= total:
                    monotonic_pairs.pop()
                
                # Only add if this is a new y value or better sum
                if not monotonic_pairs or monotonic_pairs[-1][0] != num2:
                    monotonic_pairs.append((num2, total))
                
                pair_idx += 1
            
            # Now find the maximum sum for nums2[j] >= y using binary search
            max_sum = -1
            
            # Binary search for the leftmost position where num2 >= y
            left, right = 0, len(monotonic_pairs)
            target_idx = len(monotonic_pairs)
            
            for i in range(len(monotonic_pairs)):
                if monotonic_pairs[i][0] >= y:
                    target_idx = i
                    break
            
            # Check all valid positions and find max sum
            if target_idx < len(monotonic_pairs):
                max_sum = max(pair[1] for pair in monotonic_pairs[target_idx:])
            
            result[query_idx] = max_sum
        
        return result
