from typing import List


def _sum_of_max_at_most_k(a: List[int], k: int) -> int:
    n = len(a)
    # L[i]: previous index with a[L] > a[i] (strict), else -1
    # R[i]: next index with a[R] >= a[i], else n
    L = [-1] * n
    R = [n] * n
    stack = []
    for i in range(n):
        while stack and a[stack[-1]] <= a[i]:
            R[stack.pop()] = i
        L[i] = stack[-1] if stack else -1
        stack.append(i)

    total = 0
    for i in range(n):
        lo = max(L[i] + 1, i - k + 1)  # leftmost valid start
        t = R[i] - 1                   # rightmost valid end
        if lo > i:
            continue
        m = min(i, t - k + 1)          # l <= m: r-range capped by l+k-1
        cnt_a = 0
        if m >= lo:
            c = m - lo + 1
            s_l = (lo + m) * c // 2
            cnt_a = s_l + (k - i) * c  # sum of (l + k - i)
        b_lo = max(lo, t - k + 2)      # l >= b_lo: r-range capped by t
        cnt_b = 0
        if b_lo <= i:
            cnt_b = (i - b_lo + 1) * (t - i + 1)
        total += a[i] * (cnt_a + cnt_b)
    return total


class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        return _sum_of_max_at_most_k(nums, k) - _sum_of_max_at_most_k([-x for x in nums], k)
