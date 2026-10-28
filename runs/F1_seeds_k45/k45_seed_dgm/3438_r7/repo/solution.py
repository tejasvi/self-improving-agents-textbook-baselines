class Solution:
    def countOfPeaks(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        """
        Count peaks in array with update and range query operations.
        
        A peak is an element that is strictly greater than its neighbors.
        The first and last element of an array or subarray cannot be a peak.
        """
        result = []
        
        for query in queries:
            if query[0] == 1:
                # Type 1: Count peaks in range [l, r]
                l, r = query[1], query[2]
                peak_count = 0
                
                # A peak cannot be:
                # - At the first element of the entire array (index 0)
                # - At the last element of the entire array (index len(nums)-1)
                # - At the first element of the range (index l)
                # - At the last element of the range (index r)
                # So we check from max(1, l+1) to min(len(nums)-2, r-1)
                start = max(1, l + 1)
                end = min(len(nums) - 2, r - 1)
                
                for i in range(start, end + 1):
                    # Check if nums[i] is a peak
                    if nums[i] > nums[i - 1] and nums[i] > nums[i + 1]:
                        peak_count += 1
                
                result.append(peak_count)
            else:
                # Type 2: Update nums[index] to val
                index, val = query[1], query[2]
                nums[index] = val
        
        return result
