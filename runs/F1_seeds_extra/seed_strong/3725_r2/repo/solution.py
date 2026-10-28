from typing import *


class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)

        def weighted_sum(vals: List[int]) -> int:
            # sum over subarrays of length <= k of max(subarray),
            # ties broken so each subarray is assigned to its leftmost max.
            # L[i]: previous index with vals >= vals[i] (exclusive bound)
            # R[i]: next index with vals > vals[i] (exclusive bound)
            L = [-1] * n
            R = [n] * n
            st = []
            for i in range(n):
                v = vals[i]
                while st and vals[st[-1]] < v:
                    R[st.pop()] = i
                L[i] = st[-1] if st else -1
                st.append(i)
            total = 0
            for i in range(n):
                Rr = R[i] - 1  # last valid right endpoint
                lo = max(L[i] + 1, i - k + 1)
                if lo > i:
                    continue
                # l in [lo, i]; r in [i, min(Rr, l+k-1)]
                # count(l) = min(Rr, l+k-1) - i + 1
                # part1: l <= Rr-k+1 -> count = l+k-i
                A, B = lo, min(i, Rr - k + 1)
                cnt = 0
                if A <= B:
                    m = B - A + 1
                    cnt += (A + B) * m // 2 + (k - i) * m
                # part2: l >= max(lo, Rr-k+2) -> count = Rr-i+1
                A2 = max(lo, Rr - k + 2)
                if A2 <= i:
                    cnt += (i - A2 + 1) * (Rr - i + 1)
                total += vals[i] * cnt
            return total

        return weighted_sum(nums) + weighted_sum([-x for x in nums]) * -1
