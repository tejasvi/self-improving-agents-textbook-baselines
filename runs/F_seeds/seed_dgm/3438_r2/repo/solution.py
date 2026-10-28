from typing import List


class Solution:
    def countOfPeaks(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums)
        a = list(nums)
        tree = [0] * (n + 1)

        def add(i: int, delta: int) -> None:
            i += 1
            while i <= n:
                tree[i] += delta
                i += i & (-i)

        def prefix(i: int) -> int:
            # sum of flags for indices [0, i]
            if i < 0:
                return 0
            i += 1
            s = 0
            while i > 0:
                s += tree[i]
                i -= i & (-i)
            return s

        flag = [0] * n

        def is_peak(i: int) -> int:
            if 0 < i < n - 1 and a[i] > a[i - 1] and a[i] > a[i + 1]:
                return 1
            return 0

        for i in range(1, n - 1):
            flag[i] = is_peak(i)
            if flag[i]:
                add(i, 1)

        res = []
        for q in queries:
            if q[0] == 1:
                l, r = q[1], q[2]
                if r - l < 2:
                    res.append(0)
                else:
                    res.append(prefix(r - 1) - prefix(l))
            else:
                idx, val = q[1], q[2]
                a[idx] = val
                for j in (idx - 1, idx, idx + 1):
                    if 0 < j < n - 1:
                        f = is_peak(j)
                        if f != flag[j]:
                            add(j, f - flag[j])
                            flag[j] = f
        return res
