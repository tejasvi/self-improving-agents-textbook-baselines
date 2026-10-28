from typing import List

class Solution:
    def countOfPeaks(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        """
        Count peaks in a dynamic array with update and range queries.
        
        A peak at index i means: nums[i] > nums[i-1] and nums[i] > nums[i+1]
        First and last elements cannot be peaks.
        """
        n = len(nums)
        result = []
        
        # Build a peak array where peak[i] = 1 if nums[i] is a peak, 0 otherwise
        # Only indices 1 to n-2 can be peaks
        peaks = [0] * n
        
        def update_peaks(idx):
            """Update the peak status for indices affected by a change at idx"""
            # Check if idx itself could be a peak (must be 1 to n-2)
            if 1 <= idx <= n - 2:
                if nums[idx] > nums[idx - 1] and nums[idx] > nums[idx + 1]:
                    peaks[idx] = 1
                else:
                    peaks[idx] = 0
            
            # Check if the previous element became/stopped being a peak
            if 1 <= idx - 1 <= n - 2:
                if nums[idx - 1] > nums[idx - 2] and nums[idx - 1] > nums[idx]:
                    peaks[idx - 1] = 1
                else:
                    peaks[idx - 1] = 0
            
            # Check if the next element became/stopped being a peak
            if 1 <= idx + 1 <= n - 2:
                if nums[idx + 1] > nums[idx] and nums[idx + 1] > nums[idx + 2]:
                    peaks[idx + 1] = 1
                else:
                    peaks[idx + 1] = 0
        
        # Initialize peaks array
        for i in range(1, n - 1):
            if nums[i] > nums[i - 1] and nums[i] > nums[i + 1]:
                peaks[i] = 1
        
        # Process queries
        for query in queries:
            if query[0] == 1:
                # Type 1: count peaks in range [l, r]
                l, r = query[1], query[2]
                # Peaks can only be in range [l+1, r-1] since first and last can't be peaks
                count = sum(peaks[max(1, l + 1):min(n - 1, r)])
                result.append(count)
            else:
                # Type 2: update nums[index] to val
                index, val = query[1], query[2]
                if nums[index] != val:
                    nums[index] = val
                    # Update peaks for affected indices
                    update_peaks(index)
        
        return result
