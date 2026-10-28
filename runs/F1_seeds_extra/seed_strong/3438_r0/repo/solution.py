from typing import *


class Solution:
    def countOfPeaks(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        a = list(nums)
        n = len(a)
        tree = [0] * (n + 1)

        def add(i, d):
            i += 1
            while i <= n:
                tree[i] += d
                i += i & -i

        def pref(i):  # sum over [0, i)
            s = 0
            while i > 0:
                s += tree[i]
                i -= i & -i
            return s

        def is_peak(j):
            return 1 if 0 < j < n - 1 and a[j] > a[j - 1] and a[j] > a[j + 1] else 0

        peak = [0] * n
        for j in range(1, n - 1):
            if is_peak(j):
                peak[j] = 1
                add(j, 1)

        res = []
        for q in queries:
            if q[0] == 1:
                l, r = q[1], q[2]
                if r - l < 2:
                    res.append(0)
                else:
                    res.append(pref(r) - pref(l + 1))
            else:
                idx, val = q[1], q[2]
                a[idx] = val
                for j in (idx - 1, idx, idx + 1):
                    if 0 <= j < n:
                        p = is_peak(j)
                        if p != peak[j]:
                            peak[j] = p
                            add(j, p - (1 - p))
        return res
