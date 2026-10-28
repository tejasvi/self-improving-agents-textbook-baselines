from typing import *


def _sum_max_at_most_k(nums, k):
    n = len(nums)
    # p[i]: previous index with value >= nums[i] (or -1)
    # q[i]: next index with value > nums[i] (or n)
    p = [-1] * n
    q = [n] * n
    stack = []
    for i in range(n):
        v = nums[i]
        while stack and nums[stack[-1]] < v:
            q[stack.pop()] = i
        p[i] = stack[-1] if stack else -1
        stack.append(i)
    total = 0
    for i in range(n):
        a = i - p[i]          # choices for left endpoint
        b = q[i] - i          # choices for right endpoint
        X = a if a < k else k  # x = i - l in [0, X-1]
        # count = sum_{x=0}^{X-1} min(b, k - x)
        t = k - b + 1
        if t < 0:
            t = 0
        if t > X:
            t = X
        cnt = t * b + (X - t) * k - (t + X - 1) * (X - t) // 2
        total += nums[i] * cnt
    return total


class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        return _sum_max_at_most_k(nums, k) - _sum_max_at_most_k([-v for v in nums], k)
