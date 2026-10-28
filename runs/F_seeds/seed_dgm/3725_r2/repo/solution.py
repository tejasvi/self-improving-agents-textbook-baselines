from typing import List


class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        s = k - 1

        def tri(t: int) -> int:
            # number of pairs (x, y) >= 0 with x + y <= t
            return (t + 1) * (t + 2) // 2 if t >= 0 else 0

        def count(p: int, q: int) -> int:
            # pairs x in [0, p-1], y in [0, q-1], x + y <= s
            return tri(s) - tri(s - p) - tri(s - q) + tri(s - p - q)

        def weighted_sum(arr: List[int], strict_left: bool, strict_right: bool) -> int:
            # left[i]: distance to previous element that dominates (per tie rule)
            left = [0] * n
            stack: List[int] = []
            for i in range(n):
                v = arr[i]
                if strict_left:
                    while stack and arr[stack[-1]] <= v:
                        stack.pop()
                else:
                    while stack and arr[stack[-1]] < v:
                        stack.pop()
                left[i] = i - (stack[-1] if stack else -1)
                stack.append(i)
            right = [0] * n
            stack = []
            for i in range(n - 1, -1, -1):
                v = arr[i]
                if strict_right:
                    while stack and arr[stack[-1]] <= v:
                        stack.pop()
                else:
                    while stack and arr[stack[-1]] < v:
                        stack.pop()
                right[i] = (stack[-1] if stack else n) - i
                stack.append(i)
            total = 0
            for i in range(n):
                total += arr[i] * count(left[i], right[i])
            return total

        # Ties: left boundary is previous >= element, right boundary is next > element,
        # so each subarray is attributed to exactly one max and one min index.
        mx = weighted_sum(nums, strict_left=False, strict_right=True)
        neg = [-x for x in nums]
        mn = -weighted_sum(neg, strict_left=False, strict_right=True)
        return mx + mn
