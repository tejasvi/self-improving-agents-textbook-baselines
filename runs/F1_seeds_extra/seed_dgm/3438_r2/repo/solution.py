from typing import List


class Solution:
    def countOfPeaks(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        a = list(nums)
        n = len(a)
        tree = [0] * (n + 1)

        def add(i, delta):
            i += 1
            while i <= n:
                tree[i] += delta
                i += i & (-i)

        def prefix(i):
            # sum over positions [0, i)
            s = 0
            while i > 0:
                s += tree[i]
                i -= i & (-i)
            return s

        def is_peak(i):
            return 0 < i < n - 1 and a[i] > a[i - 1] and a[i] > a[i + 1]

        cur = [0] * n
        for i in range(1, n - 1):
            if is_peak(i):
                cur[i] = 1
                add(i, 1)

        def refresh(i):
            if 0 <= i < n:
                p = 1 if is_peak(i) else 0
                if p != cur[i]:
                    add(i, p - cur[i])
                    cur[i] = p

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
                    refresh(j)
        return res
