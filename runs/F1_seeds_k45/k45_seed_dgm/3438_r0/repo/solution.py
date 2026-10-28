class Solution:
    def countOfPeaks(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums)
        
        # Track which positions are peaks
        is_peak = [False] * n
        
        # Helper function to check if position i is a peak
        def check_peak(i):
            if i <= 0 or i >= n - 1:
                return False
            return nums[i] > nums[i - 1] and nums[i] > nums[i + 1]
        
        # Initialize peaks
        for i in range(1, n - 1):
            is_peak[i] = check_peak(i)
        
        # Build prefix sum array for quick range queries
        def build_prefix_sum():
            prefix = [0] * (n + 1)
            for i in range(n):
                prefix[i + 1] = prefix[i] + (1 if is_peak[i] else 0)
            return prefix
        
        prefix_sum = build_prefix_sum()
        result = []
        
        for query in queries:
            if query[0] == 1:
                # Count peaks in range [l, r]
                l, r = query[1], query[2]
                # Count peaks in the range [l, r]
                # Peaks can only be at positions from l+1 to r-1 (not at boundaries)
                if l + 1 > r - 1:
                    # No valid positions for peaks
                    result.append(0)
                else:
                    # Sum of peaks from l+1 to r-1 (inclusive)
                    count = prefix_sum[r] - prefix_sum[l + 1]
                    result.append(count)
            else:
                # Update query
                index, val = query[1], query[2]
                nums[index] = val
                
                # Check which positions might have changed peak status
                # Only positions index-1, index, index+1 can be affected
                for i in [index - 1, index, index + 1]:
                    if 0 < i < n - 1:
                        is_peak[i] = check_peak(i)
                
                # Rebuild prefix sum
                prefix_sum = build_prefix_sum()
        
        return result
