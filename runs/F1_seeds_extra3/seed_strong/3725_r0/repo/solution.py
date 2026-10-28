from typing import *


def _sum_max_at_most_k(a: List[int], k: int) -> int:
    n = len(a)
    # left[i]: nearest j<i with a[j] >= a[i], else -1
    left = [-1] * n
    stack = []
    for i in range(n):
        v = a[i]
        while stack and a[stack[-1]] < v:
            stack.pop()
        left[i] = stack[-1] if stack else -1
        stack.append(i)
    # right[i]: nearest j>i with a[j] > a[i], else n
    right = [n] * n
    stack = []
    for i in range(n - 1, -1, -1):
        v = a[i]
        while stack and a[stack[-1]] <= v:
            stack.pop()
        right[i] = stack[-1] if stack else n
        stack.append(i)

    total = 0
    for i in range(n):
        lo = max(i - k + 1, left[i] + 1)  # valid start indices l in [lo, i]
        b = right[i] - 1                  # valid end indices r in [i, b]
        # Part 1: l <= b-k+1 -> count of r = l+k-i
        x, y = lo, min(i, b - k + 1)
        cnt_sum = 0
        if x <= y:
            m = y - x + 1
            cnt_sum += (x + y) * m // 2 + (k - i) * m
        # Part 2: l >= b-k+2 -> count of r = b-i+1
        x2 = max(lo, b - k + 2)
        y2 = i
        if x2 <= y2:
            cnt_sum += (b - i + 1) * (y2 - x2 + 1)
        total += a[i] * cnt_sum
    return total


class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        smax = _sum_max_at_most_k(nums, k)
        smin = -_sum_max_at_most_k([-x for x in nums], k)
        return smax + smin
