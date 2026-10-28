from typing import *


class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        K = k - 1  # max extra elements on both sides combined

        def count(x: int, y: int) -> int:
            # number of pairs (p, q) with 0<=p<=x, 0<=q<=y, p+q<=K
            xp = min(x, K)
            if xp < 0:
                return 0
            a = max(0, K - y)  # for p >= a, q ranges over [0, K-p] (K-p <= y)
            total = 0
            m = min(a - 1, xp)  # p in [0, m]: q count = y+1
            if m >= 0:
                total += (m + 1) * (y + 1)
            lo = max(a, 0)
            if lo <= xp:
                # sum of (K-p+1) for p in [lo, xp]
                first = K - lo + 1
                last = K - xp + 1
                total += (first + last) * (first - last + 1) // 2
            return total

        def contributions(arr: List[int]) -> List[int]:
            # For each i: subarrays where i is the max, with tie-break:
            # left stops at prev with arr>=arr[i]; right stops at next with arr>arr[i].
            L = [-1] * n
            R = [n] * n
            st: List[int] = []
            for i in range(n):
                v = arr[i]
                while st and arr[st[-1]] < v:
                    st.pop()
                L[i] = st[-1] if st else -1
                st.append(i)
            st = []
            for i in range(n - 1, -1, -1):
                v = arr[i]
                while st and arr[st[-1]] <= v:
                    st.pop()
                R[i] = st[-1] if st else n
                st.append(i)
            return [count(i - L[i] - 1, R[i] - i - 1) for i in range(n)]

        cmax = contributions(nums)
        cneg = contributions([-v for v in nums])
        # sum of max = sum cmax*v ; sum of min = -(sum of max of negated) = sum cneg*v
        return sum((cmax[i] + cneg[i]) * nums[i] for i in range(n))
