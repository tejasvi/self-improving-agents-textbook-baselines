from typing import List

class Solution:
    def maxValue(self, nums: List[int], k: int) -> int:
        """
        Find the maximum value of a subsequence of size 2*k.
        
        The value is defined as:
        (OR of first k elements in subsequence) XOR (OR of last k elements in subsequence)
        
        Key insight:
        - We can split at any position i: select k elements from nums[0:i+1]
          as the left part, and k elements from nums[i+1:] as the right part
        - Use DP to compute all possible OR values for selecting j elements from any prefix/suffix
        """
        n = len(nums)
        
        # left[i][j] = set of all possible OR values when selecting exactly j elements
        #              from the first i elements of nums
        left = [[set() for _ in range(k + 1)] for _ in range(n + 1)]
        left[0][0].add(0)
        
        for i in range(n):
            for j in range(k + 1):
                # Don't take nums[i]
                left[i + 1][j] = left[i + 1][j].union(left[i][j])
                # Take nums[i]
                if j > 0:
                    for val in left[i][j - 1]:
                        left[i + 1][j].add(val | nums[i])
        
        # right[i][j] = set of all possible OR values when selecting exactly j elements
        #               from nums[i:] (i.e., from position i to the end)
        right = [[set() for _ in range(k + 1)] for _ in range(n + 1)]
        right[n][0].add(0)
        
        for i in range(n - 1, -1, -1):
            for j in range(k + 1):
                # Don't take nums[i]
                right[i][j] = right[i][j].union(right[i + 1][j])
                # Take nums[i]
                if j > 0:
                    for val in right[i + 1][j - 1]:
                        right[i][j].add(val | nums[i])
        
        # Find maximum XOR value
        # Try all split points i: left part uses elements from [0, i), right part from [i, n)
        max_val = 0
        for i in range(n + 1):
            # We need exactly k elements from left[0:i] and k from right[i:n]
            left_or_set = left[i][k]
            right_or_set = right[i][k]
            
            for left_or in left_or_set:
                for right_or in right_or_set:
                    max_val = max(max_val, left_or ^ right_or)
        
        return max_val
