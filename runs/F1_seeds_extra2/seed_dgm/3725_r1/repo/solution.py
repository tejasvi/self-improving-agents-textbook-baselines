from typing import List


class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        K = k - 1

        def T(m: int) -> int:
            # number of pairs (x, y) >= 0 with x + y <= m
            return (m + 1) * (m + 2) // 2 if m >= 0 else 0

        def count(a: int, b: int) -> int:
            # pairs x in [0, a), y in [0, b) with x + y <= K
            return T(K) - T(K - a) - T(K - b) + T(K - a - b)

        def contributions(greater: bool) -> List[int]:
            # For each i, number of valid subarrays where nums[i] is the
            # max (greater=True) or min (greater=False), with tie-breaking.
            left = [-1] * n
            right = [n] * n
            stack = []
            for i in range(n):
                v = nums[i]
                while stack and (
                    nums[stack[-1]] <= v if greater else nums[stack[-1]] >= v
                ):
                    stack.pop()
                left[i] = stack[-1] if stack else -1
                stack.append(i)
            stack = []
            for i in range(n - 1, -1, -1):
                v = nums[i]
                while stack and (
                    nums[stack[-1]] < v if greater else nums[stack[-1]] > v
                ):
                    stack.pop()
                right[i] = stack[-1] if stack else n
                stack.append(i)
            return [count(i - left[i], right[i] - i) for i in range(n)]

        cmax = contributions(True)
        cmin = contributions(False)
        total = 0
        for i in range(n):
            total += nums[i] * (cmax[i] + cmin[i])
        return total
