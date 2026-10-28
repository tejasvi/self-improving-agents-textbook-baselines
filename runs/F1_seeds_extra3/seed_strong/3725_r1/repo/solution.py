from typing import *


class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        K = k - 1

        def g(m):
            # number of (x, y) with x, y >= 0 and x + y <= m
            if m < 0:
                return 0
            return (m + 1) * (m + 2) // 2

        def count(p, q):
            # number of (x, y) with 0 <= x < p, 0 <= y < q, x + y <= K
            return g(K) - g(K - p) - g(K - q) + g(K - p - q)

        def ranges(arr, strict_left_greater):
            # For each i: left[i] = distance to previous element that dominates (exclusive),
            # right[i] = distance to next element that dominates (inclusive tie-break).
            # Dominance for max: prev uses >, next uses >=; for min mirrored.
            L = [0] * n
            R = [0] * n
            st = []
            for i in range(n):
                while st and arr[st[-1]] < arr[i]:
                    st.pop()
                L[i] = i - (st[-1] if st else -1)
                st.append(i)
            st = []
            for i in range(n - 1, -1, -1):
                while st and arr[st[-1]] <= arr[i]:
                    st.pop()
                R[i] = (st[-1] if st else n) - i
                st.append(i)
            return L, R

        # max: prev strictly smaller popped (prev is >=), next popped if <= -> strict on right
        # Use one consistent tie-break: left side uses '<' popping (prev >= ends range),
        # right side uses '<=' popping (next > ends range). Each subarray gets exactly one max owner.
        Lmax, Rmax = ranges(nums, True)
        neg = [-x for x in nums]
        Lmin, Rmin = ranges(neg, True)

        total = 0
        for i in range(n):
            cmax = count(Lmax[i], Rmax[i])
            cmin = count(Lmin[i], Rmin[i])
            total += nums[i] * (cmax + cmin)
        return total
