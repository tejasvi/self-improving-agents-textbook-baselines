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
                i += i & -i

        def prefix(i):  # sum of indicators over [0, i]
            i += 1
            s = 0
            while i > 0:
                s += tree[i]
                i -= i & -i
            return s

        def is_peak(i):
            return 1 if arr[i] > arr[i - 1] and arr[i] > arr[i + 1] else 0

        peak = [0] * n
        for i in range(1, n - 1):
            if is_peak(i):
                peak[i] = 1
                add(i, 1)

        def refresh(i):
            if 1 <= i <= n - 2:
                v = is_peak(i)
                if v != peak[i]:
                    add(i, v - peak[i])
                    peak[i] = v

        answer = []
        for q in queries:
            if q[0] == 1:
                l, r = q[1], q[2]
                lo = max(l + 1, 1)
                hi = min(r - 1, n - 2)
                if lo > hi:
                    answer.append(0)
                else:
                    answer.append(prefix(hi) - prefix(lo - 1))
            else:
                idx, val = q[1], q[2]
                arr[idx] = val
                for j in (idx - 1, idx, idx + 1):
                    refresh(j)
        return answer
