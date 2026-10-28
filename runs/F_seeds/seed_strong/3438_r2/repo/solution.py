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

        def prefix(i):
            # sum of flags over indices [0, i)
            s = 0
            while i > 0:
                s += tree[i]
                i -= i & -i
            return s

        flag = [0] * n

        def is_peak(i):
            return 1 if 0 < i < n - 1 and a[i - 1] < a[i] > a[i + 1] else 0

        for i in range(1, n - 1):
            if is_peak(i):
                flag[i] = 1
                add(i, 1)

        res = []
        for q in queries:
            if q[0] == 1:
                l, r = q[1], q[2]
                if r - l < 2:
                    res.append(0)
                else:
                    res.append(prefix(r) - prefix(l + 1))
            else:
                idx, val = q[1], q[2]
                a[idx] = val
                for j in (idx - 1, idx, idx + 1):
                    if 0 <= j < n:
                        p = is_peak(j)
                        if p != flag[j]:
                            add(j, p - flag[j])
                            flag[j] = p
        return res
