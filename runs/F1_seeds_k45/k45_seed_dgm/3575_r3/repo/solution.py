from typing import List

class Solution:
    def maxValue(self, nums: List[int], k: int) -> int:
        """
        Find the maximum value of a subsequence of size 2*k.
        The value is defined as: (OR of first k elements) XOR (OR of last k elements)
        
        Approach:
        - Use dynamic programming to compute all possible OR values we can achieve
          by selecting exactly i elements from the first j elements of the array
        - For each possible split point, compute all possible OR values for the left half
          and all possible OR values for the right half
        - Find the maximum XOR between any OR value from left and any from right
        """
        n = len(nums)
        
        # dp_left[j][i] = set of OR values when selecting exactly i elements from first j elements
        dp_left = [[set() for _ in range(k + 1)] for _ in range(n + 1)]
        for i in range(n + 1):
            dp_left[i][0].add(0)
        
        for j in range(n):
            for i in range(k + 1):
                # Don't take nums[j]
                dp_left[j + 1][i] = dp_left[j + 1][i].union(dp_left[j][i])
                # Take nums[j]
                if i > 0:
                    for prev_or in dp_left[j][i - 1]:
                        dp_left[j + 1][i].add(prev_or | nums[j])
        
        # dp_right[j][i] = set of OR values when selecting i elements from last (n-j) elements
        dp_right = [[set() for _ in range(k + 1)] for _ in range(n + 1)]
        for i in range(n + 1):
            dp_right[i][0].add(0)
        
        for j in range(n - 1, -1, -1):
            for i in range(k + 1):
                # Don't take nums[j]
                dp_right[j][i] = dp_right[j][i].union(dp_right[j + 1][i])
                # Take nums[j]
                if i > 0:
                    for prev_or in dp_right[j + 1][i - 1]:
                        dp_right[j][i].add(prev_or | nums[j])
        
        # Now compute the answer
        # For each split point j, compute max XOR between:
        # - k elements from first j elements
        # - k elements from last (n-j) elements
        max_value = 0
        for j in range(k, n - k + 1):
            left_ors = dp_left[j][k]
            right_ors = dp_right[j][k]
            for left_or in left_ors:
                for right_or in right_ors:
                    max_value = max(max_value, left_or ^ right_or)
        
        return max_value
