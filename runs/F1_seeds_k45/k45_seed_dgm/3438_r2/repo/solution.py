from typing import List

class Solution:
    def countOfPeaks(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        """
        Process queries on an array to count peaks and update values.
        
        A peak at index i is defined as: nums[i] > nums[i-1] and nums[i] > nums[i+1]
        Peaks cannot exist at the first or last indices of a subarray.
        
        Query type 1: [1, l, r] - count peaks in nums[l..r]
        Query type 2: [2, index, val] - set nums[index] = val
        """
        n = len(nums)
        result = []
        
        # Helper function to check if index i is a peak
        def is_peak(i):
            if i <= 0 or i >= n - 1:
                return False
            return nums[i] > nums[i - 1] and nums[i] > nums[i + 1]
        
        # Precompute peaks array
        # peaks[i] = 1 if nums[i] is a peak, 0 otherwise
        peaks = [0] * n
        for i in range(1, n - 1):
            if nums[i] > nums[i - 1] and nums[i] > nums[i + 1]:
                peaks[i] = 1
        
        # Precompute prefix sum for fast range queries
        prefix = [0] * (n + 1)
        for i in range(n):
            prefix[i + 1] = prefix[i] + peaks[i]
        
        # Process queries
        for query in queries:
            if query[0] == 1:
                # Type 1: Count peaks in range [l, r]
                l, r = query[1], query[2]
                # Peaks can only be from index l+1 to r-1 (not at boundaries)
                # So we count peaks from l+1 to r-1 inclusive
                if l + 1 > r - 1:
                    # No valid positions for peaks
                    result.append(0)
                else:
                    # Sum of peaks from index l+1 to r-1
                    count = prefix[r] - prefix[l + 1]
                    result.append(count)
            else:
                # Type 2: Update nums[index] to val
                index = query[1]
                val = query[2]
                
                if nums[index] == val:
                    # No change needed
                    continue
                
                nums[index] = val
                
                # Update peaks array and prefix sums
                # Only indices index-1, index, index+1 can be affected
                for i in range(max(1, index - 1), min(n - 1, index + 2)):
                    new_peak = 1 if is_peak(i) else 0
                    
                    if peaks[i] != new_peak:
                        # Update prefix sums from position i+1 onwards
                        diff = new_peak - peaks[i]
                        peaks[i] = new_peak
                        for j in range(i + 1, n + 1):
                            prefix[j] += diff
        
        return result
