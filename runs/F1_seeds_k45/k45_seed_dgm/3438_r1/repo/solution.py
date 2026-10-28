class Solution:
    def countOfPeaks(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums)
        
        # Helper function to check if index i is a peak
        def is_peak(i):
            if i <= 0 or i >= n - 1:
                return False
            return nums[i - 1] < nums[i] > nums[i + 1]
        
        # Initialize peaks array - 1 if peak, 0 otherwise
        peaks = [0] * n
        for i in range(1, n - 1):
            if is_peak(i):
                peaks[i] = 1
        
        # Prefix sum array for fast range queries
        prefix = [0] * (n + 1)
        for i in range(n):
            prefix[i + 1] = prefix[i] + peaks[i]
        
        result = []
        
        for query in queries:
            if query[0] == 1:
                # Count peaks in range [l, r]
                l, r = query[1], query[2]
                # Count peaks in range [l, r]
                # peaks[i] can only exist for i in [1, n-2]
                # So we count peaks from max(1, l) to min(n-2, r)
                left = max(1, l)
                right = min(n - 2, r)
                if left <= right:
                    count = prefix[right + 1] - prefix[left]
                else:
                    count = 0
                result.append(count)
            else:
                # Update nums[index] to val
                index, val = query[1], query[2]
                nums[index] = val
                
                # Update peak status for indices that might be affected
                # An index i can be a peak only if it depends on i-1, i, i+1
                # So updating nums[index] affects peaks at indices index-1, index, index+1
                for i in range(max(1, index - 1), min(n - 1, index + 2)):
                    old_peak = peaks[i]
                    new_peak = 1 if is_peak(i) else 0
                    if old_peak != new_peak:
                        peaks[i] = new_peak
                        # Update prefix sum from position i+1 onwards
                        for j in range(i + 1, n + 1):
                            prefix[j] += (new_peak - old_peak)
        
        return result
