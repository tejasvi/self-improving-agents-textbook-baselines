from typing import List

class Solution:
    def maximumSumQueries(self, nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
        """
        Find maximum sum for each query with constraints.
        
        The key insight is to:
        1. Sort pairs by nums1 in descending order
        2. Sort queries by x in descending order with original indices
        3. Process queries in descending order of x, maintaining a monotonic stack of candidates
        4. Use coordinate compression on y values for efficient lookup
        """
        n = len(nums1)
        m = len(queries)
        
        # Create pairs of (nums1[i], nums2[i], sum) and sort by nums1 descending
        pairs = sorted([(nums1[i], nums2[i], nums1[i] + nums2[i]) for i in range(n)], reverse=True)
        
        # Create queries with original indices: (x, y, original_index)
        indexed_queries = [(queries[i][0], queries[i][1], i) for i in range(m)]
        # Sort by x in descending order
        indexed_queries.sort(reverse=True)
        
        result = [-1] * m
        
        # Monotonic stack to keep track of (nums2, sum) pairs
        # We maintain pairs where nums2 is decreasing and sum is increasing
        mono_stack = []
        
        pair_idx = 0
        
        for x, y, orig_idx in indexed_queries:
            # Add all pairs with nums1[j] >= x to the stack
            while pair_idx < n and pairs[pair_idx][0] >= x:
                nums1_val, nums2_val, sum_val = pairs[pair_idx]
                
                # Remove elements from stack that have nums2 <= current nums2 (redundant)
                # We only keep (nums2, sum) pairs where nums2 is strictly decreasing
                while mono_stack and mono_stack[-1][0] <= nums2_val:
                    mono_stack.pop()
                
                # Add this pair to stack (update max sum if same nums2 appears again)
                if mono_stack and mono_stack[-1][1] >= sum_val:
                    # This sum is not better than what's already there for similar nums2
                    pair_idx += 1
                    continue
                
                mono_stack.append((nums2_val, sum_val))
                pair_idx += 1
            
            # Binary search for the largest nums2 >= y in the stack
            # The stack has nums2 in decreasing order
            left, right = 0, len(mono_stack) - 1
            best = -1
            
            while left <= right:
                mid = (left + right) // 2
                if mono_stack[mid][0] >= y:
                    best = mid
                    left = mid + 1
                else:
                    right = mid - 1
            
            if best != -1:
                result[orig_idx] = mono_stack[best][1]
        
        return result
