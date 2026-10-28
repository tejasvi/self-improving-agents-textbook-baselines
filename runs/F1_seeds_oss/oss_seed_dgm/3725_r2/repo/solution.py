from typing import List

class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        """Return sum of (max + min) over all subarrays with length at most k.
        
        For each element we count how many subarrays (with length ≤ k) have that
        element as the maximum (or minimum).  Its contribution is value * count.
        The count is the number of pairs (a, b) where:
            a = distance to the left bound (0‑based),
            b = distance to the right bound (0‑based),
            a < left_len, b < right_len,
            a + b + 1 ≤ k  →  a + b ≤ k‑1.
        left_len/right_len are the sizes of the maximal interval where the
        element is the unique maximum (or minimum) using a monotonic stack.
        """
        n = len(nums)
        limit = k - 1  # maximum allowed sum of left and right distances

        # ---------- helper to count pairs (a,b) with a+b ≤ limit ----------
        def count_pairs(a: int, b: int, limit: int) -> int:
            if limit < 0:
                return 0
            if a == 0 or b == 0:
                return 0
            # ensure a <= b for simpler case analysis
            if a > b:
                a, b = b, a
            max_sum = a + b - 2  # maximum possible a+b
            if limit >= max_sum:
                return a * b

            if limit < a:
                # triangular number for limit+1 values (0..limit)
                return (limit + 1) * (limit + 2) // 2
            if limit >= b - 1:
                # exclude the pairs where a+b > limit
                t = max_sum - limit
                return a * b - t * (t + 1) // 2
            # a <= limit < b-1
            # a_max is limited by both a-1 and limit, but in this branch limit < b-1
            a_max = limit  # because limit < b-1 and a <= limit (otherwise handled above)
            # sum_{x=0}^{a_max} (limit - x + 1)
            return (a_max + 1) * (limit + 1) - (a_max * (a_max + 1) // 2)

        # ---------- compute contributions for maximums ----------
        # previous greater (strict) to the left
        left_dist = [0] * n
        stack = []  # indices with decreasing values
        for i, val in enumerate(nums):
            while stack and nums[stack[-1]] <= val:
                stack.pop()
            prev = stack[-1] if stack else -1
            left_dist[i] = i - prev
            stack.append(i)

        # next greater or equal to the right
        right_dist = [0] * n
        stack.clear()
        for i in range(n - 1, -1, -1):
            val = nums[i]
            while stack and nums[stack[-1]] < val:
                stack.pop()
            nxt = stack[-1] if stack else n
            right_dist[i] = nxt - i
            stack.append(i)

        total_max = 0
        for i in range(n):
            cnt = count_pairs(left_dist[i], right_dist[i], limit)
            total_max += nums[i] * cnt

        # ---------- compute contributions for minimums ----------
        # previous smaller (strict) to the left
        left_dist = [0] * n
        stack.clear()
        for i, val in enumerate(nums):
            while stack and nums[stack[-1]] >= val:
                stack.pop()
            prev = stack[-1] if stack else -1
            left_dist[i] = i - prev
            stack.append(i)

        # next smaller or equal to the right
        right_dist = [0] * n
        stack.clear()
        for i in range(n - 1, -1, -1):
            val = nums[i]
            while stack and nums[stack[-1]] > val:
                stack.pop()
            nxt = stack[-1] if stack else n
            right_dist[i] = nxt - i
            stack.append(i)

        total_min = 0
        for i in range(n):
            cnt = count_pairs(left_dist[i], right_dist[i], limit)
            total_min += nums[i] * cnt

        return total_max + total_min
