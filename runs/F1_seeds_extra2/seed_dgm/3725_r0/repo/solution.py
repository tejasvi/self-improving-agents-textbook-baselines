from typing import List


class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        K = k - 1  # max extra elements beyond the anchor

        def g(t: int) -> int:
            # number of (x, y) with x, y >= 0 and x + y <= t
            if t < 0:
                return 0
            return (t + 1) * (t + 2) // 2

        def count(p: int, q: int) -> int:
            # number of (x, y) with 0<=x<=p, 0<=y<=q, x+y<=K
            return g(K) - g(K - p - 1) - g(K - q - 1) + g(K - p - q - 2)

        def contribution(is_max: bool) -> int:
            # Each index i is the anchor (max or min, with tie-breaking) of
            # subarrays [i-x, i+y] where x in [0,L[i]], y in [0,R[i]].
            if is_max:
                # left blocks on >=, right blocks on >
                pop_left = lambda top, v: nums[top] < v
                pop_right = lambda top, v: nums[top] <= v
            else:
                pop_left = lambda top, v: nums[top] > v
                pop_right = lambda top, v: nums[top] >= v
            L = [0] * n
            R = [0] * n
            stack = []
            for i in range(n):
                v = nums[i]
                while stack and pop_left(stack[-1], v):
                    stack.pop()
                L[i] = i - (stack[-1] if stack else -1) - 1
                stack.append(i)
            stack = []
            for i in range(n - 1, -1, -1):
                v = nums[i]
                while stack and pop_right(stack[-1], v):
                    stack.pop()
                R[i] = (stack[-1] if stack else n) - i - 1
                stack.append(i)
            total = 0
            for i in range(n):
                total += nums[i] * count(min(L[i], K), min(R[i], K))
            return total

        return contribution(True) + contribution(False)
