from typing import List


class Solution:
    def countOfPeaks(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        arr = list(nums)
        n = len(arr)
        tree = [0] * (n + 1)

        def add(i: int, delta: int) -> None:
            i += 1
            while i <= n:
                tree[i] += delta
                i += i & (-i)

        def prefix(i: int) -> int:
            # sum of indicators for positions [0, i]
            if i < 0:
                return 0
            i += 1
            s = 0
            while i > 0:
                s += tree[i]
                i -= i & (-i)
            return s

        def is_peak(i: int) -> int:
            if 0 < i < n - 1 and arr[i] > arr[i - 1] and arr[i] > arr[i + 1]:
                return 1
            return 0

        status = [0] * n
        for i in range(1, n - 1):
            status[i] = is_peak(i)
            if status[i]:
                add(i, 1)

        answer = []
        for q in queries:
            if q[0] == 1:
                l, r = q[1], q[2]
                answer.append(prefix(r - 1) - prefix(l) if r - l >= 2 else 0)
            else:
                idx, val = q[1], q[2]
                arr[idx] = val
                for j in (idx - 1, idx, idx + 1):
                    if 0 <= j < n:
                        new = is_peak(j)
                        if new != status[j]:
                            add(j, new - status[j])
                            status[j] = new
        return answer
