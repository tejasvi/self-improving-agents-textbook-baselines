from typing import List


class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        K = k - 1

        def T(m: int) -> int:
            # number of pairs (x, y) with x, y >= 0 and x + y <= m
            return (m + 1) * (m + 2) // 2 if m >= 0 else 0

        def count(a: int, b: int) -> int:
            # pairs (x, y), 0 <= x < a, 0 <= y < b, x + y <= K
            return T(K) - T(K - a) - T(K - b) + T(K - a - b)

        def role_sum(vals: List[int]) -> int:
            # Sum over subarrays of length <= k of max(vals).
            # Each subarray is attributed to its leftmost maximum:
            # L = previous index with vals >= vals[i]
            # R = next index with vals > vals[i]
            L = [-1] * n
            R = [n] * n
            stack = []
            for i in range(n):
                while stack and vals[stack[-1]] < vals[i]:
                    R[stack.pop()] = i
                stack.append(i)
            stack = []
            for i in range(n):
                while stack and vals[stack[-1]] < vals[i]:
                    stack.pop()
                L[i] = stack[-1] if stack else -1
                stack.append(i)
            total = 0
            for i in range(n):
                total += vals[i] * count(i - L[i], R[i] - i)
            return total

        # sum of max - sum of min, where min(w) = -max(-w)
        return role_sum(nums) - role_sum([-v for v in nums])
