from typing import List


def _count_pairs(A: int, B: int, m: int) -> int:
    """Count pairs (a, b) with 0<=a<=A, 0<=b<=B, a+b<=m (closed form)."""
    if A < 0 or B < 0 or m < 0:
        return 0
    A = min(A, m)
    total = 0
    # a in [0, t]: all B+1 values of b are allowed
    t = min(A, m - B)
    if t >= 0:
        total += (t + 1) * (B + 1)
    # a in [lo, A]: b in [0, m-a]
    lo = max(0, m - B + 1)
    hi = A
    if hi >= lo:
        cnt = hi - lo + 1
        first = m - hi + 1
        last = m - lo + 1
        total += (first + last) * cnt // 2
    return total


class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        m = k - 1
        if n == 0:
            return 0

        def side(is_max: bool) -> int:
            # Ties are broken asymmetrically (strict on left, non-strict on
            # right) so each subarray's extreme is attributed to one index.
            left = [-1] * n
            right = [n] * n
            stack = []
            for i in range(n):
                v = nums[i]
                if is_max:
                    while stack and nums[stack[-1]] < v:
                        stack.pop()
                else:
                    while stack and nums[stack[-1]] > v:
                        stack.pop()
                left[i] = stack[-1] if stack else -1
                stack.append(i)
            stack = []
            for i in range(n - 1, -1, -1):
                v = nums[i]
                if is_max:
                    while stack and nums[stack[-1]] <= v:
                        stack.pop()
                else:
                    while stack and nums[stack[-1]] >= v:
                        stack.pop()
                right[i] = stack[-1] if stack else n
                stack.append(i)
            s = 0
            for i in range(n):
                A = i - left[i] - 1
                B = right[i] - i - 1
                s += nums[i] * _count_pairs(A, B, m)
            return s

        return side(True) + side(False)
