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

        def prefix(i):  # sum over [0, i]
            i += 1
            s = 0
            while i > 0:
                s += tree[i]
                i -= i & (-i)
            return s

        is_peak = [0] * n

        def is_p(i):
            return 1 if arr[i] > arr[i - 1] and arr[i] > arr[i + 1] else 0

        for i in range(1, n - 1):
            if is_p(i):
                is_peak[i] = 1
                add(i, 1)

        res = []
        for q in queries:
            if q[0] == 1:
                l, r = q[1], q[2]
                lo = max(l + 1, 1)
                hi = min(r - 1, n - 2)
                if lo > hi:
                    res.append(0)
                else:
                    res.append(prefix(hi) - prefix(lo - 1))
            else:
                idx, val = q[1], q[2]
                arr[idx] = val
                for p in (idx - 1, idx, idx + 1):
                    if 1 <= p <= n - 2:
                        new = is_p(p)
                        if new != is_peak[p]:
                            is_peak[p] = new
                            add(p, 1 if new else -1)
        return res
