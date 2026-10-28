from typing import List


class Solution:
    def countOfPeaks(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums)
        arr = list(nums)
        tree = [0] * (n + 1)

        def add(i: int, delta: int) -> None:
            i += 1
            while i <= n:
                tree[i] += delta
                i += i & (-i)

        def prefix(i: int) -> int:
            # sum over indices [0, i]
            i += 1
            s = 0
            while i > 0:
                s += tree[i]
                i -= i & (-i)
            return s

        is_peak = [0] * n

        def is_p(i: int) -> int:
            if 1 <= i <= n - 2 and arr[i] > arr[i - 1] and arr[i] > arr[i + 1]:
                return 1
            return 0

        for i in range(1, n - 1):
            is_peak[i] = is_p(i)
            if is_peak[i]:
                add(i, 1)

        answer = []
        for q in queries:
            if q[0] == 1:
                l, r = q[1], q[2]
                if r - l < 2:
                    answer.append(0)
                    continue
                answer.append(prefix(r - 1) - prefix(l))
            else:
                idx, val = q[1], q[2]
                arr[idx] = val
                for j in (idx - 1, idx, idx + 1):
                    if 1 <= j <= n - 2:
                        new = is_p(j)
                        if new != is_peak[j]:
                            add(j, new - is_peak[j])
                            is_peak[j] = new
        return answer
