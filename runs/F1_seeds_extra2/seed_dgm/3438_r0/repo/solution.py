from typing import List


class Solution:
    def countOfPeaks(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums)
        arr = list(nums)
        tree = [0] * (n + 1)

        def add(i, delta):
            i += 1
            while i <= n:
                tree[i] += delta
                i += i & (-i)

        def prefix(i):
            # sum of flags over indices [0, i)
            s = 0
            while i > 0:
                s += tree[i]
                i -= i & (-i)
            return s

        def is_peak(i):
            return 1 if 0 < i < n - 1 and arr[i] > arr[i - 1] and arr[i] > arr[i + 1] else 0

        flag = [0] * n
        for i in range(1, n - 1):
            if is_peak(i):
                flag[i] = 1
                add(i, 1)

        res = []
        for q in queries:
            if q[0] == 1:
                l, r = q[1], q[2]
                # peaks strictly inside (l, r)
                if r - l < 2:
                    res.append(0)
                else:
                    res.append(prefix(r) - prefix(l + 1))
            else:
                idx, val = q[1], q[2]
                arr[idx] = val
                for j in (idx - 1, idx, idx + 1):
                    if 0 <= j < n:
                        p = is_peak(j)
                        if p != flag[j]:
                            add(j, p - flag[j])
                            flag[j] = p
        return res
