"""
Solution for maximum-and-minimum-sums-of-at-most-size-k-subarrays problem.
Implements efficient O(n) algorithm using monotonic stacks and combinatorial counting.
"""

from typing import List

class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        if n == 0:
            return 0
        # helper to count pairs (left choices, right choices) giving length <= k
        def count_pairs(L: int, R: int) -> int:
            # L, R are positive integers (distances to boundaries)
            B = k - 1  # max allowed a+b where a,b are offsets from the element
            max_a = min(L - 1, B)
            if max_a < 0:
                return 0
            # t = B - R ; for a <= t term = R else term = B - a
            t = B - R
            cnt1 = 0
            if t >= 0:
                cnt1 = min(max_a, t) + 1  # number of a where term = R
            # region 2 start index
            a2 = max(t + 1, 0) if t >= 0 else 0
            if a2 > max_a:
                n2 = 0
            else:
                n2 = max_a - a2 + 1
            # sum of (B - a) for a in [a2, max_a]
            # = n2*B - sum_{a2}^{max_a} a
            sum_a = (a2 + max_a) * n2 // 2 if n2 > 0 else 0
            cnt2 = n2 * B - sum_a
            return R * cnt1 + cnt2

        # ----- minimum contribution -----
        # previous less (strict) distances
        left = [0] * n
        stack = []  # will store indices with increasing values
        for i, val in enumerate(nums):
            while stack and nums[stack[-1]] >= val:
                stack.pop()
            prev = stack[-1] if stack else -1
            left[i] = i - prev
            stack.append(i)
        # next less-or-equal distances
        right = [0] * n
        stack.clear()
        for i in range(n - 1, -1, -1):
            val = nums[i]
            while stack and nums[stack[-1]] > val:
                stack.pop()
            nxt = stack[-1] if stack else n
            right[i] = nxt - i
            stack.append(i)
        sum_min = 0
        for i in range(n):
            cnt = count_pairs(left[i], right[i])
            sum_min += nums[i] * cnt

        # ----- maximum contribution -----
        # previous greater (strict) distances
        left_max = [0] * n
        stack.clear()
        for i, val in enumerate(nums):
            while stack and nums[stack[-1]] <= val:
                stack.pop()
            prev = stack[-1] if stack else -1
            left_max[i] = i - prev
            stack.append(i)
        # next greater-or-equal distances
        right_max = [0] * n
        stack.clear()
        for i in range(n - 1, -1, -1):
            val = nums[i]
            while stack and nums[stack[-1]] < val:
                stack.pop()
            nxt = stack[-1] if stack else n
            right_max[i] = nxt - i
            stack.append(i)
        sum_max = 0
        for i in range(n):
            cnt = count_pairs(left_max[i], right_max[i])
            sum_max += nums[i] * cnt

        return sum_min + sum_max
