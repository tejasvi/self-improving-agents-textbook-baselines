from typing import List


class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)

        def count(A: int, B: int) -> int:
            # A: max left extent, B: max right extent (from index i).
            # Count pairs (x, y), 0<=x<=A, 0<=y<=B, x+y<=k-1.
            X = min(A, k - 1)
            if X < 0:
                return 0
            T = min(X, k - 1 - B)  # x in [0, T] gives full B+1 choices
            total = 0
            s = 0
            if T >= 0:
                total += (T + 1) * (B + 1)
                s = T + 1
            if s <= X:
                # sum over x in [s, X] of (k - x)
                cnt = X - s + 1
                total += (k - s + k - X) * cnt // 2
            return total

        def contribution(arr):
            # sum over subarrays (len<=k) of max(arr[l..r]) with tie-breaking.
            L = [0] * n  # left extent
            R = [0] * n  # right extent
            stack = []
            for i in range(n):
                # previous strictly greater
                while stack and arr[stack[-1]] <= arr[i]:
                    stack.pop()
                prev = stack[-1] if stack else -1
                L[i] = i - prev - 1
                stack.append(i)
            stack = []
            for i in range(n - 1, -1, -1):
                # next greater-or-equal
                while stack and arr[stack[-1]] < arr[i]:
                    stack.pop()
                nxt = stack[-1] if stack else n
                R[i] = nxt - i - 1
                stack.append(i)
            total = 0
            for i in range(n):
                total += arr[i] * count(L[i], R[i])
            return total

        mx = contribution(nums)
        mn = contribution([-v for v in nums])
        return mx - mn
