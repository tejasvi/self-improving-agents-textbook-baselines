from typing import List


class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        def max_sum(arr):
            # Sum over all subarrays (length <= k) of their maximum.
            # Each subarray is assigned to its leftmost maximum index i:
            # left part strictly smaller than arr[i], right part <= arr[i].
            n = len(arr)
            prev = [-1] * n
            nxt = [n] * n
            st = []
            for i in range(n):
                v = arr[i]
                while st and arr[st[-1]] < v:
                    st.pop()
                prev[i] = st[-1] if st else -1
                st.append(i)
            st = []
            for i in range(n - 1, -1, -1):
                v = arr[i]
                while st and arr[st[-1]] <= v:
                    st.pop()
                nxt[i] = st[-1] if st else n
                st.append(i)

            total = 0
            for i in range(n):
                L = prev[i] + 1  # start a in [L, i]
                R = nxt[i] - 1   # end b in [i, R]
                # count pairs (a, b): L <= a <= i <= b <= R, b - a <= k - 1
                lo = max(L, i - k + 1)
                # Case 1: a + k - 1 <= R  -> number of b is a + k - i
                hi1 = min(i, R - k + 1)
                cnt = 0
                if hi1 >= lo:
                    m = hi1 - lo + 1
                    first = lo + k - i
                    last = hi1 + k - i
                    cnt += (first + last) * m // 2
                # Case 2: a + k - 1 > R -> number of b is R - i + 1
                lo2 = max(lo, R - k + 2)
                if lo2 <= i:
                    cnt += (i - lo2 + 1) * (R - i + 1)
                total += arr[i] * cnt
            return total

        neg = [-x for x in nums]
        # sum of minima = -(sum of maxima of negated array)
        return max_sum(nums) - max_sum(neg)
