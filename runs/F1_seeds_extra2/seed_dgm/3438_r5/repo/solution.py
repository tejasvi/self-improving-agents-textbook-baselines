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

        def prefix(i):  # sum of flags on [0, i)
            s = 0
            while i > 0:
                s += tree[i]
                i -= i & -i
            return s

        def is_peak(j):
            return 1 <= j <= n - 2 and arr[j] > arr[j - 1] and arr[j] > arr[j + 1]

        flags = [0] * n
        for j in range(1, n - 1):
            if is_peak(j):
                flags[j] = 1
                add(j, 1)

        answer = []
        for q in queries:
            if q[0] == 1:
                l, r = q[1], q[2]
                if r - l < 2:
                    answer.append(0)
                else:
                    answer.append(prefix(r) - prefix(l + 1))
            else:
                idx, val = q[1], q[2]
                arr[idx] = val
                for j in (idx - 1, idx, idx + 1):
                    if 0 <= j < n:
                        now = 1 if is_peak(j) else 0
                        if now != flags[j]:
                            flags[j] = now
                            add(j, 1 if now else -1)
        return answer
