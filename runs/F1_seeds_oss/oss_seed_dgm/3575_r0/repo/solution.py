from typing import List

class Solution:
    def maxValue(self, nums: List[int], k: int) -> int:
        n = len(nums)
        # dp_left[i][j] = set of OR values using exactly j elements from first i elements
        dp_left = [[set() for _ in range(k + 1)] for _ in range(n + 1)]
        dp_left[0][0].add(0)
        for i in range(1, n + 1):
            num = nums[i - 1]
            for j in range(k + 1):
                # not take current element
                dp_left[i][j] = dp_left[i - 1][j].copy()
                if j > 0:
                    for v in dp_left[i - 1][j - 1]:
                        dp_left[i][j].add(v | num)
        # dp_right[i][j] = set of OR values using exactly j elements from suffix starting at i
        dp_right = [[set() for _ in range(k + 1)] for _ in range(n + 1)]
        dp_right[n][0].add(0)
        for i in range(n - 1, -1, -1):
            num = nums[i]
            for j in range(k + 1):
                # not take current element
                dp_right[i][j] = dp_right[i + 1][j].copy()
                if j > 0:
                    for v in dp_right[i + 1][j - 1]:
                        dp_right[i][j].add(v | num)
        ans = 0
        # split point p: left uses first p elements, right uses from p onward
        for p in range(n + 1):
            left_set = dp_left[p][k]
            right_set = dp_right[p][k]
            if not left_set or not right_set:
                continue
            for a in left_set:
                for b in right_set:
                    val = a ^ b
                    if val > ans:
                        ans = val
        return ans
