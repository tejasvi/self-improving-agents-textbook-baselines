from typing import List

class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        """Return the sum of the maximum and minimum elements of all subarrays
        with length at most k.

        The contribution of each element as a minimum (or maximum) can be counted
        using monotonic stacks to find the range where it is the unique minimum (or
        maximum). For each element at index i we know:
            left  = i - prev   (distance to previous smaller/greater element)
            right = next - i   (distance to next   smaller/greater element)
        Any subarray where this element is the min (or max) must choose a left part
        length a (1 <= a <= left) and a right part length b (1 <= b <= right).
        Its total length is a + b - 1 and must satisfy a + b - 1 <= k.
        The number of valid (a, b) pairs is:
            sum_{a=1}^{min(left, k)} min(right, k - a + 1)
        The above sum can be evaluated in O(1) using arithmetic series.
        We compute this contribution for minima and maxima separately and add
        the results.
        """
        n = len(nums)
        if n == 0:
            return 0

        # Helper to compute sum_{a=1}^{maxA} min(right, k - a + 1)
        def count_contrib(left: int, right: int) -> int:
            # a can be at most left and also cannot exceed k (because a + b -1 <= k).
            maxA = left if left < k else k
            # For a given a, the maximal allowed b is k - a + 1.
            # If that value is >= right, min(right, ...) == right.
            # The threshold where it switches is when a > k - right + 1.
            # Let t = max(1, k - right + 1). For a < t we get right, for a >= t we get k - a + 1.
            t = k - right + 1
            if t < 1:
                t = 1
            if t > maxA:
                # All a give min = right
                return maxA * right
            # a from 1 .. t-1 => contribution right each
            fixed = (t - 1) * right
            # a from t .. maxA => contribution (k - a + 1)
            cnt = maxA - t + 1
            # arithmetic series: (first + last) * cnt // 2
            first = k - t + 1
            last = k - maxA + 1
            variable = (first + last) * cnt // 2
            return fixed + variable

        # ---------- minima contribution ----------
        prev_less = [-1] * n  # index of previous element strictly less
        stack = []
        for i, x in enumerate(nums):
            while stack and nums[stack[-1]] >= x:
                stack.pop()
            prev_less[i] = stack[-1] if stack else -1
            stack.append(i)

        next_less = [n] * n  # index of next element less or equal
        stack.clear()
        for i in range(n - 1, -1, -1):
            x = nums[i]
            while stack and nums[stack[-1]] > x:
                stack.pop()
            next_less[i] = stack[-1] if stack else n
            stack.append(i)

        sum_min = 0
        for i in range(n):
            left = i - prev_less[i]
            right = next_less[i] - i
            cnt = count_contrib(left, right)
            sum_min += nums[i] * cnt

        # ---------- maxima contribution ----------
        prev_greater = [-1] * n  # index of previous element strictly greater
        stack.clear()
        for i, x in enumerate(nums):
            while stack and nums[stack[-1]] <= x:
                stack.pop()
            prev_greater[i] = stack[-1] if stack else -1
            stack.append(i)

        next_greater = [n] * n  # index of next element greater or equal
        stack.clear()
        for i in range(n - 1, -1, -1):
            x = nums[i]
            while stack and nums[stack[-1]] < x:
                stack.pop()
            next_greater[i] = stack[-1] if stack else n
            stack.append(i)

        sum_max = 0
        for i in range(n):
            left = i - prev_greater[i]
            right = next_greater[i] - i
            cnt = count_contrib(left, right)
            sum_max += nums[i] * cnt

        return sum_min + sum_max
