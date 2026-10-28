from typing import List


class Solution:
    def countOfPeaks(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums)
        arr = list(nums)
        flag = [0] * n
        tree = [0] * (n + 1)

        def add(i, d):
            i += 1
            while i <= n:
                tree[i] += d
                i += i & (-i)

        def prefix(i):  # sum of flags over [0, i]
            i += 1
            s = 0
            while i > 0:
                s += tree[i]
                i -= i & (-i)
            return s

        def is_peak(i):
            return 1 <= i <= n - 2 and arr[i] > arr[i - 1] and arr[i] > arr[i + 1]

        for i in range(n):
            if is_peak(i):
                flag[i] = 1
                add(i, 1)

        res = []
        for t, a, b in queries:
            if t == 1:
                l, r = a, b
                if r - l < 2:
                    res.append(0)
                else:
                    res.append(prefix(r - 1) - prefix(l))
            else:
                idx, val = a, b
                arr[idx] = val
                for j in range(max(0, idx - 1), min(n, idx + 2)):
                    p = 1 if is_peak(j) else 0
                    if p != flag[j]:
                        add(j, p - flag[j])
                        flag[j] = p
        return res
