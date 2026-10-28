from typing import *


class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        K = k - 1

        def h(m: int) -> int:
            # number of pairs (a, b) >= 0 with a + b <= m
            if m < 0:
                return 0
            return (m + 1) * (m + 2) // 2

        def count(A: int, B: int) -> int:
            # pairs a in [0, A), b in [0, B), a + b <= K
            return h(K) - h(K - A) - h(K - B) + h(K - A - B)

        def extents(strict_left: bool):
            # For each i: A = number of choices for left offset, B for right.
            # Left boundary: previous element that is >= (for max) / <= (for min).
            # Right boundary: next element that is > (for max) / < (for min).
            left = [0] * n
            right = [0] * n
            st = []
            for i in range(n):
                v = nums[i]
                if strict_left:  # max: pop while nums[top] < v, prev is >= v
                    while st and nums[st[-1]] < v:
                        st.pop()
                else:  # min: pop while nums[top] > v
                    while st and nums[st[-1]] > v:
                        st.pop()
                left[i] = i - (st[-1] if st else -1)
                st.append(i)
            st = []
            for i in range(n - 1, -1, -1):
                v = nums[i]
                if strict_left:  # next strictly greater
                    while st and nums[st[-1]] <= v:
                        st.pop()
                else:  # next strictly smaller
                    while st and nums[st[-1]] >= v:
                        st.pop()
                right[i] = (st[-1] if st else n) - i
                st.append(i)
            return left, right

        total = 0
        for is_max in (True, False):
            L, R = extents(is_max)
            s = 0
            for i in range(n):
                s += nums[i] * count(L[i], R[i])
            total += s
        return total
