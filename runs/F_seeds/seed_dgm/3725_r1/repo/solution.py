from typing import List


class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        K = k - 1

        def count(A: int, B: int) -> int:
            # number of pairs (a, b), 0<=a<=A, 0<=b<=B, a+b<=K
            Ap = min(A, K)
            if Ap < 0:
                return 0
            if K - B >= 0:
                p = min(Ap, K - B)
            else:
                p = -1
            total = (p + 1) * (B + 1)
            m = Ap - p
            if m > 0:
                first = K - p
                last = K + 1 - Ap
                total += m * (first + last) // 2
            return total

        def contribution(vals):
            # i owns subarrays where it is the maximum, ties broken to the leftmost-owner:
            # L = previous index with vals >= vals[i]; R = next index with vals > vals[i]
            L = [-1] * n
            R = [n] * n
            stack = []
            for i in range(n):
                v = vals[i]
                while stack and vals[stack[-1]] < v:
                    stack.pop()
                L[i] = stack[-1] if stack else -1
                stack.append(i)
            stack = []
            for i in range(n - 1, -1, -1):
                v = vals[i]
                while stack and vals[stack[-1]] <= v:
                    stack.pop()
                R[i] = stack[-1] if stack else n
                stack.append(i)
            total = 0
            for i in range(n):
                A = i - L[i] - 1
                B = R[i] - i - 1
                total += vals[i] * count(A, B)
            return total

        mx = contribution(nums)
        mn = -contribution([-x for x in nums])
        return mx + mn
