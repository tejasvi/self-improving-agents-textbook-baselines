from typing import List


class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        K = k - 1

        def T(m: int) -> int:
            # number of pairs (x, y) >= 0 with x + y <= m
            if m < 0:
                return 0
            return (m + 1) * (m + 2) // 2

        def count(a: int, b: int) -> int:
            # pairs x in [0, a-1], y in [0, b-1], x + y <= K
            return T(K) - T(K - a) - T(K - b) + T(K - a - b)

        def contributions(is_max: bool) -> List[int]:
            # left[i]: number of valid left endpoints for i (i - prev boundary)
            # right[i]: number of valid right endpoints for i (next boundary - i)
            left = [0] * n
            right = [0] * n
            stack = []
            for i in range(n):
                v = nums[i]
                if is_max:
                    while stack and nums[stack[-1]] < v:
                        right[stack.pop()] = i
                else:
                    while stack and nums[stack[-1]] > v:
                        right[stack.pop()] = i
                left[i] = i - (stack[-1] if stack else -1)
                stack.append(i)
            for j in stack:
                right[j] = n
            # right currently holds the boundary index; convert to counts
            return [count(left[i], right[i] - i) for i in range(n)]

        cmax = contributions(True)
        cmin = contributions(False)
        total = 0
        for i in range(n):
            total += nums[i] * (cmax[i] + cmin[i])
        return total
