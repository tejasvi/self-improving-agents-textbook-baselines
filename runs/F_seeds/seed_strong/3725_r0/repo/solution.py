from typing import *


def _tri(n: int) -> int:
    # number of (x, y) with x, y >= 0 and x + y <= n
    if n < 0:
        return 0
    return (n + 1) * (n + 2) // 2


def _sum_max(a: List[int], k: int) -> int:
    n = len(a)
    m = k - 1
    # left[i]: index of previous element >= a[i] (or -1)
    # right[i]: index of next element > a[i] (or n)
    left = [-1] * n
    right = [n] * n
    st: List[int] = []
    for i in range(n):
        while st and a[st[-1]] < a[i]:
            right[st.pop()] = i
        left[i] = st[-1] if st else -1
        st.append(i)
    total = 0
    for i in range(n):
        p = i - left[i] - 1  # choices on left (x in [0, p])
        q = right[i] - i - 1  # choices on right (y in [0, q])
        cnt = _tri(m) - _tri(m - p - 1) - _tri(m - q - 1) + _tri(m - p - q - 2)
        total += a[i] * cnt
    return total


class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        return _sum_max(nums, k) - _sum_max([-x for x in nums], k)
