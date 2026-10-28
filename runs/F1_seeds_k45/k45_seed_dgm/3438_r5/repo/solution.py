from typing import List

class Solution:
    def countOfPeaks(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums)
        
        # Helper function to check if index i is a peak
        def is_peak(index):
            if index <= 0 or index >= n - 1:
                return False
            return nums[index] > nums[index - 1] and nums[index] > nums[index + 1]
        
        # Build initial peak array where peak[i] = 1 if nums[i] is a peak, 0 otherwise
        peak = [0] * n
        for i in range(1, n - 1):
            if is_peak(i):
                peak[i] = 1
        
        # Build prefix sum array for efficient range sum queries
        prefix = [0] * (n + 1)
        for i in range(n):
            prefix[i + 1] = prefix[i] + peak[i]
        
        answer = []
        
        for query in queries:
            if query[0] == 1:
                # Count peaks in range [l, r]
                l, r = query[1], query[2]
                # We can only have peaks in range [l+1, r-1] since first and last can't be peaks
                if l + 1 > r - 1:
                    answer.append(0)
                else:
                    # Count peaks in range [l+1, r-1] using prefix sum
                    count = prefix[r] - prefix[l + 1]
                    answer.append(count)
            else:
                # Update nums[index] to val
                index, val = query[1], query[2]
                nums[index] = val
                
                # After update, we need to update peak array and prefix sum
                # Only positions index-1, index, index+1 can be affected
                for pos in [index - 1, index, index + 1]:
                    if 0 < pos < n - 1:
                        old_peak = peak[pos]
                        new_peak = 1 if is_peak(pos) else 0
                        
                        # Update peak array
                        peak[pos] = new_peak
                        
                        # Update prefix sum array from pos onwards
                        diff = new_peak - old_peak
                        for j in range(pos + 1, n + 1):
                            prefix[j] += diff
        
        return answer
