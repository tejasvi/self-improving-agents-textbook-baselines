from typing import List

class Solution:
    def maxValue(self, nums: List[int], k: int) -> int:
        """
        Find the maximum value of a subsequence of size 2*k.
        Value = (OR of first k elements) XOR (OR of last k elements)
        """
        n = len(nums)
        
        # DP to find all possible OR values when selecting exactly j elements
        # from the first i elements
        # dp_left[i][j] = set of all possible OR values when selecting j elements from first i elements
        # dp_right[i][j] = set of all possible OR values when selecting j elements from last (n-i) elements
        
        # For left half: select k elements and compute possible OR values
        dp_left = [[set() for _ in range(k + 1)] for _ in range(n + 1)]
        dp_left[0][0].add(0)  # Base case: select 0 elements, OR = 0
        
        for i in range(1, n + 1):
            for j in range(k + 1):
                # Don't take nums[i-1]
                dp_left[i][j] = dp_left[i][j].union(dp_left[i-1][j])
                
                # Take nums[i-1]
                if j > 0:
                    for val in dp_left[i-1][j-1]:
                        dp_left[i][j].add(val | nums[i-1])
        
        # For right half: select k elements from remaining and compute possible OR values
        # We process from right to left
        dp_right = [[set() for _ in range(k + 1)] for _ in range(n + 1)]
        dp_right[n][0].add(0)  # Base case: select 0 elements, OR = 0
        
        for i in range(n - 1, -1, -1):
            for j in range(k + 1):
                # Don't take nums[i]
                dp_right[i][j] = dp_right[i][j].union(dp_right[i+1][j])
                
                # Take nums[i]
                if j > 0:
                    for val in dp_right[i+1][j-1]:
                        dp_right[i][j].add(val | nums[i])
        
        # Now we need to find the best combination
        # For each way to select k elements from left half,
        # we can select remaining elements for right half
        max_value = 0
        
        # Try all ways to split the selection
        for i in range(k, n - k + 1):  # i is the number of elements we've processed from left
            # From first i elements, select exactly k
            # From remaining (n-i) elements, select exactly k
            if n - i >= k:
                for or_left in dp_left[i][k]:
                    for or_right in dp_right[i][k]:
                        max_value = max(max_value, or_left ^ or_right)
        
        return max_value
