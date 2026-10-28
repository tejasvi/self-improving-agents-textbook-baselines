from typing import List

class Solution:
    def countOfPeaks(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums)
        
        # is_peak[i] = 1 if nums[i] is a peak, 0 otherwise
        # Index 0 and n-1 cannot be peaks
        is_peak = [0] * n
        
        def update_peak(idx):
            """Update the peak status at index idx"""
            if idx <= 0 or idx >= n - 1:
                is_peak[idx] = 0
                return
            
            if nums[idx] > nums[idx - 1] and nums[idx] > nums[idx + 1]:
                is_peak[idx] = 1
            else:
                is_peak[idx] = 0
        
        # Initialize peaks for all positions
        for i in range(1, n - 1):
            update_peak(i)
        
        # prefix[i] = number of peaks in nums[0..i-1]
        def build_prefix():
            prefix = [0] * (n + 1)
            for i in range(1, n + 1):
                prefix[i] = prefix[i - 1] + is_peak[i - 1]
            return prefix
        
        prefix = build_prefix()
        result = []
        
        for query in queries:
            if query[0] == 1:
                # Count peaks in subarray [l, r]
                l, r = query[1], query[2]
                # peaks in [l, r] are elements at indices (l+1) to (r-1)
                # because first and last cannot be peaks
                if r - l <= 1:
                    # No middle elements, so no peaks
                    result.append(0)
                else:
                    # Count peaks in range [l+1, r-1]
                    # prefix[r] - prefix[l+1] gives peaks in [l+1, r-1]
                    count = prefix[r] - prefix[l + 1]
                    result.append(count)
            else:
                # Update query: nums[index] = val
                idx, val = query[1], query[2]
                if nums[idx] != val:
                    nums[idx] = val
                    
                    # Update peaks that could be affected
                    # Only peaks at idx-1, idx, idx+1 could change
                    for affected_idx in [idx - 1, idx, idx + 1]:
                        old_peak = is_peak[affected_idx]
                        update_peak(affected_idx)
                        new_peak = is_peak[affected_idx]
                        
                        # Update prefix array if peak status changed
                        if old_peak != new_peak:
                            diff = new_peak - old_peak
                            for i in range(affected_idx + 1, n + 1):
                                prefix[i] += diff
        
        return result
