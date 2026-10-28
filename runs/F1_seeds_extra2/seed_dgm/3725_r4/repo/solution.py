from typing import List


class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)

        def contribution(a: List[int]) -> int:
            # Sum over all subarrays of length <= k of max(a).
            # Index i is the leftmost maximum of [l, r] iff
            #   L < l <= i <= r < R
            # where L = previous index with a[L] >= a[i] (or -1),
            #       R = next index with a[R] > a[i] (or n).
            L = [-1] * n
            R = [n] * n
            st = []
            for i in range(n):
                v = a[i]
                while st and a[st[-1]] < v:
                    st.pop()
                L[i] = st[-1] if st else -1
                st.append(i)
            st = []
            for i in range(n - 1, -1, -1):
                v = a[i]
                while st and a[st[-1]] <= v:
                    st.pop()
                R[i] = st[-1] if st else n
                st.append(i)

            total = 0
            for i in range(n):
                Ri = R[i]
                lo = max(L[i] + 1, i - k + 1)  # smallest valid l
                if lo > i:
                    continue
                cnt = 0
                # l in [lo, A]: r in [i, l+k-1], count = l + k - i
                A = min(i, Ri - k)
                if A >= lo:
                    m = A - lo + 1
                    s = (lo + A) * m // 2
                    cnt += s + m * (k - i)
                # l in [B, i]: r in [i, Ri-1], count = Ri - i
                B = max(lo, A + 1)
                if B <= i:
                    cnt += (i - B + 1) * (Ri - i)
                total += a[i] * cnt
            return total

        # max + min = max(nums) + (-max(-nums))
        return contribution(list(nums)) - contribution([-x for x in nums])
