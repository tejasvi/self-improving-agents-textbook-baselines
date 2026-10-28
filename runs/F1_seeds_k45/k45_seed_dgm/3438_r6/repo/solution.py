from typing import List

class Solution:
    def countOfPeaks(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        """
        Count peaks in subarrays and handle updates.
        
        A peak is an element that is greater than both its previous and next element.
        First and last elements cannot be peaks.
        
        Query type 1: [1, l, r] - count peaks in nums[l:r+1]
        Query type 2: [2, index, val] - update nums[index] to val
        """
        result = []
        
        # Helper function to check if an index is a peak
        def is_peak(idx):
            if idx <= 0 or idx >= len(nums) - 1:
                return False
            return nums[idx] > nums[idx - 1] and nums[idx] > nums[idx + 1]
        
        # Process each query
        for query in queries:
            if query[0] == 1:
                # Type 1: Count peaks in subarray [l, r]
                l, r = query[1], query[2]
                count = 0
                # Peaks can only start from index 1 (since first element can't be peak)
                # and can only go up to r-1 (since last element can't be peak)
                for i in range(max(1, l), min(r, len(nums) - 1) + 1):
                    if is_peak(i):
                        count += 1
                result.append(count)
            else:
                # Type 2: Update element at index
                index, val = query[1], query[2]
                nums[index] = val
        
        return result
