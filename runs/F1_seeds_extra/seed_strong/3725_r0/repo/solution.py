from typing import *


class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)

        def contrib(vals, sign_strict_left):
            # For each i: left extent a (count of l choices), right extent b (count of r choices).
            # Ties broken: left side uses strict, right side uses non-strict comparison.
            left = [0] * n
            stack = []
            for i in range(n):
                v = vals[i]
                if sign_strict_left:
                    while stack and vals[stack[-1]] < v:
                        stack.pop()
                else:
                    while stack and vals[stack[-1]] > v:
                        stack.pop()
                left[i] = i - (stack[-1] if stack else -1)
                stack.append(i)
            right = [0] * n
            stack = []
            for i in range(n - 1, -1, -1):
                v = vals[i]
                if sign_strict_left:
                    while stack and vals[stack[-1]] <= v:
                        stack.pop()
                else:
                    while stack and vals[stack[-1]] >= v:
                        stack.pop()
                right[i] = (stack[-1] if stack else n) - i
                stack.append(i)
            total = 0
            for i in range(n):
                a = left[i]
                b = right[i]
                m = min(a, k)  # x in [0, m)
                # count(x) = min(b, k - x)
                t = k - b + 1
                if t < 0:
                    t = 0
                if t > m:
                    t = m
                # x in [0, t): contributes b each
                s = t * b
                # x in [t, m): contributes k - x
                c = m - t
                if c > 0:
                    s += c * k - (t + m - 1) * c // 2
                total += vals[i] * s
            return total

        mx = contrib(nums, True)
        neg = [-x for x in nums]
        mn = -contrib(neg, True)
        return mx + mn
